#!/usr/bin/env python3

from __future__ import annotations

import math
from typing import List, Tuple

import rclpy
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from scipy.spatial.transform import Rotation


class PurePursuitPlanner(Node):
    def __init__(self) -> None:
        super().__init__("pure_pursuit_planner")

        # Parameters
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("drive_topic", "/drive")
        self.declare_parameter("lookahead_distance", 1.5)
        self.declare_parameter("target_speed", 0.6)
        self.declare_parameter("wheelbase", 0.33)
        self.declare_parameter("control_rate_hz", 20.0)

        self.odom_topic = self.get_parameter("odom_topic").value
        self.drive_topic = self.get_parameter("drive_topic").value
        self.lookahead_distance = float(self.get_parameter("lookahead_distance").value)
        self.target_speed = float(self.get_parameter("target_speed").value)
        self.wheelbase = float(self.get_parameter("wheelbase").value)
        self.control_rate_hz = float(self.get_parameter("control_rate_hz").value)

        # State from odometry
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.odom_received = False

        # A simple example waypoint path in odom frame
        # Replace these with your real track points later.
        self.waypoints: List[Tuple[float, float]] = [

            (0.5, 0.5),
            (1.5, 0.5),
            (2.5, -0.5),
            (3.5, -0.5),
            (4.5, -0.5),
            (5.5, 0.5),
            (6.5, 0.5),
            (7.5, -0.5),
            (8.5, -0.5),
            (9.5, 0.5),

        ]
        self.current_waypoint_index = 0

        # ROS interfaces
        self.odom_sub = self.create_subscription(
            Odometry,
            self.odom_topic,
            self._on_odom,
            10,
        )

        self.drive_pub = self.create_publisher(
            AckermannDriveStamped,
            self.drive_topic,
            10,
        )

        period = 1.0 / self.control_rate_hz if self.control_rate_hz > 0.0 else 0.05
        self.timer = self.create_timer(period, self._on_timer)

        self.get_logger().info("Pure Pursuit planner started.")
        self.get_logger().info(f"odom_topic: {self.odom_topic}")
        self.get_logger().info(f"drive_topic: {self.drive_topic}")
        self.get_logger().info(f"lookahead_distance: {self.lookahead_distance}")
        self.get_logger().info(f"target_speed: {self.target_speed}")
        self.get_logger().info(f"wheelbase: {self.wheelbase}")

    def _on_odom(self, msg: Odometry) -> None:
        self.x = float(msg.pose.pose.position.x)
        self.y = float(msg.pose.pose.position.y)

        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]
        self.yaw = float(Rotation.from_quat(quat).as_euler("xyz")[2])

        self.odom_received = True


    def _on_timer(self) -> None:
        if not self.odom_received or not self.waypoints:
            return

        final_x, final_y = self.waypoints[-1]
        final_dist = math.hypot(final_x - self.x, final_y - self.y)

        if self.current_waypoint_index >= len(self.waypoints) - 1 and final_dist < 0.5:
            drive_msg = AckermannDriveStamped()
            drive_msg.header.stamp = self.get_clock().now().to_msg()
            drive_msg.header.frame_id = "base_link"
            drive_msg.drive.speed = 0.0
            drive_msg.drive.steering_angle = 0.0
            self.drive_pub.publish(drive_msg)
            return

        target_point = self._find_lookahead_point()
        if target_point is None:
            return

        steering = self._compute_steering_angle(target_point)

        drive_msg = AckermannDriveStamped()
        drive_msg.header.stamp = self.get_clock().now().to_msg()
        drive_msg.header.frame_id = "base_link"
        drive_msg.drive.speed = float(self.target_speed)
        drive_msg.drive.steering_angle = float(steering)
        self.drive_pub.publish(drive_msg)



    def _find_lookahead_point(self) -> Tuple[float, float] | None:
        """
        Find the first waypoint at least lookahead_distance ahead of the robot.
        If none is found, use the final waypoint.
        """
        for i in range(self.current_waypoint_index, len(self.waypoints)):
            wx, wy = self.waypoints[i]
            dist = math.hypot(wx - self.x, wy - self.y)
            if dist >= self.lookahead_distance:
                self.current_waypoint_index = i
                return wx, wy
            


        if self.waypoints:
            self.current_waypoint_index = len(self.waypoints) - 1
            return self.waypoints[-1]

        return None

    def _compute_steering_angle(self, target_point: Tuple[float, float]) -> float:
        """
        Pure Pursuit steering law.
        """
        tx, ty = target_point

        dx = tx - self.x
        dy = ty - self.y

        # Transform target into vehicle frame
        local_x = math.cos(-self.yaw) * dx - math.sin(-self.yaw) * dy
        local_y = math.sin(-self.yaw) * dx + math.cos(-self.yaw) * dy

        # If the point is behind us, do not try to steer to it aggressively
        if local_x <= 0.0:
            return 0.0

        # Curvature and steering
        ld2 = local_x * local_x + local_y * local_y
        if ld2 < 1e-6:
            return 0.0

        curvature = 2.0 * local_y / ld2
        steering = math.atan(self.wheelbase * curvature)

        return steering


def main() -> None:
    rclpy.init()
    node = PurePursuitPlanner()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Pure Pursuit planner interrupted by user.")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()