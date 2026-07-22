#!/usr/bin/env python3

from __future__ import annotations

import math

import rclpy
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from scipy.spatial.transform import Rotation
from typing import List, Tuple, Sequence

from .controllers.pure_pursuit import PurePursuitController
from .planners.waypoint_manager import WaypointManager
from .utils.vehicle_state import VehicleState


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
        self.declare_parameter(
            "waypoint_file",
            "/ros2_ws/src/my_f1tenth_bridge/assets/waypoints/levine_centerline.csv",
        )

        # self.declare_parameter(
        #     "waypoints_flat",
        #     [
        #         0.5, 0.5,
        #         1.5, 0.5,
        #         2.5, -0.5,
        #         3.5, -0.5,
        #         4.5, -0.5,
        #         5.5, 0.5,
        #         6.5, 0.5,
        #         7.5, -0.5,
        #         8.5, -0.5,
        #         9.5, 0.5,
        #     ],
        # )

        self.odom_topic = self.get_parameter("odom_topic").value
        self.drive_topic = self.get_parameter("drive_topic").value
        self.lookahead_distance = float(self.get_parameter("lookahead_distance").value)
        self.target_speed = float(self.get_parameter("target_speed").value)
        self.wheelbase = float(self.get_parameter("wheelbase").value)
        self.control_rate_hz = float(self.get_parameter("control_rate_hz").value)
        

        # Controller
        self.controller = PurePursuitController(self.wheelbase)

        # State from odometry
        self.state = VehicleState()
        self.odom_received = False

        # Waypoints

        # waypoints_flat = self.get_parameter("waypoints_flat").value
        # self.waypoint_manager = WaypointManager(self._parse_waypoints(waypoints_flat))

        waypoint_file = self.get_parameter("waypoint_file").value
        self.waypoint_manager = WaypointManager()
        self.waypoint_manager.load_from_csv(waypoint_file)  



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
        self.state.x = float(msg.pose.pose.position.x)
        self.state.y = float(msg.pose.pose.position.y)
        

        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]
        self.state.yaw = float(Rotation.from_quat(quat).as_euler("xyz")[2])

        self.odom_received = True

        self.state.speed = float(msg.twist.twist.linear.x)


    # def _parse_waypoints(self, flat: Sequence[float]) -> List[Tuple[float, float]]:
    #     values = [float(v) for v in flat]
    #     if len(values) % 2 != 0:
    #         raise ValueError("waypoints_flat must contain an even number of values")

    #     return [(values[i], values[i + 1]) for i in range(0, len(values), 2)]

    def _on_timer(self) -> None:
        if not self.odom_received or not self.waypoint_manager.waypoints:
            return

        final_x, final_y = self.waypoint_manager.waypoints[-1]
        final_dist = math.hypot(final_x - self.state.x, final_y - self.state.y)

        # Stop at the end of the path
        if (
            self.waypoint_manager.current_waypoint_index >= len(self.waypoint_manager.waypoints) - 1
            and final_dist < 0.5
        ):
            drive_msg = AckermannDriveStamped()
            drive_msg.header.stamp = self.get_clock().now().to_msg()
            drive_msg.header.frame_id = "base_link"
            drive_msg.drive.speed = 0.0
            drive_msg.drive.steering_angle = 0.0
            self.drive_pub.publish(drive_msg)
            return

        target_point = self.waypoint_manager.get_lookahead_point(
            self.state.x,
            self.state.y,
            self.lookahead_distance,
        )

        if target_point is None:
            return

        steering = self.controller.compute_steering(
            state=self.state,
            target_point=target_point,
        )

        drive_msg = AckermannDriveStamped()
        drive_msg.header.stamp = self.get_clock().now().to_msg()
        drive_msg.header.frame_id = "base_link"
        drive_msg.drive.speed = float(self.target_speed)
        drive_msg.drive.steering_angle = float(steering)
        self.drive_pub.publish(drive_msg)


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