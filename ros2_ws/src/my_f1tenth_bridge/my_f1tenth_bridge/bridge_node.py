#!/usr/bin/env python3

from __future__ import annotations

import numpy as np
import gymnasium as gym
import f110_gym  # noqa: F401  # registers the f110_gym environment
import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from scipy.spatial.transform import Rotation
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
# from tf_transformations import quaternion_from_euler
from ackermann_msgs.msg import AckermannDriveStamped



class BridgeNode(Node):
    def __init__(self) -> None:
        super().__init__("bridge")

        # Parameters
        self.declare_parameter("map_path", "/ros2_ws/src/my_f1tenth_bridge/assets/maps/levine")
        self.declare_parameter("map_ext", ".png")
        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("drive_topic", "/drive")

        self.declare_parameter("frame_id", "laser_model")
        self.declare_parameter("odom_frame", "odom")
        self.declare_parameter("base_frame", "base_link")
        self.declare_parameter("scan_rate_hz", 10.0)
        self.declare_parameter("scan_angle_min", -2.35)
        self.declare_parameter("scan_angle_max", 2.35)
        self.declare_parameter("range_min", 0.0)
        self.declare_parameter("range_max", 30.0)
        self.declare_parameter("initial_x", 0.0)
        self.declare_parameter("initial_y", 0.0)
        self.declare_parameter("initial_theta", 0.0)



        self.map_path = self.get_parameter("map_path").value
        self.map_ext = self.get_parameter("map_ext").value
        self.scan_topic = self.get_parameter("scan_topic").value
        self.odom_topic = self.get_parameter("odom_topic").value
        self.drive_topic = self.get_parameter("drive_topic").value
        self.frame_id = self.get_parameter("frame_id").value
        self.odom_frame = self.get_parameter("odom_frame").value
        self.base_frame = self.get_parameter("base_frame").value
        self.scan_rate_hz = float(self.get_parameter("scan_rate_hz").value)
        self.scan_angle_min = float(self.get_parameter("scan_angle_min").value)
        self.scan_angle_max = float(self.get_parameter("scan_angle_max").value)
        self.range_min = float(self.get_parameter("range_min").value)
        self.range_max = float(self.get_parameter("range_max").value)
        self.initial_x = float(self.get_parameter("initial_x").value)
        self.initial_y = float(self.get_parameter("initial_y").value)
        self.initial_theta = float(self.get_parameter("initial_theta").value)

        self.current_speed = 0.0
        self.current_steering = 0.0


        # QoS for sensor data
        scan_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
        )

        # 2. Publishers
        self.scan_pub = self.create_publisher(LaserScan, self.scan_topic, scan_qos)
        self.odom_pub = self.create_publisher(Odometry, self.odom_topic, 10)



        # 3. Subscribers
        self.drive_sub = self.create_subscription(
            AckermannDriveStamped,
            self.drive_topic,
            self._on_drive,
            10,
        )

        # 4. TF broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)


        self.get_logger().info("Bridge node started.")
        self.get_logger().info(f"map_path: {self.map_path}")
        self.get_logger().info(f"map_ext: {self.map_ext}")
        self.get_logger().info(f"scan_topic: {self.scan_topic}")
        self.get_logger().info(f"odom_topic: {self.odom_topic}")
        self.get_logger().info(f"drive_topic: {self.drive_topic}")
        self.get_logger().info(f"frame_id: {self.frame_id}")
        self.get_logger().info(f"odom_frame: {self.odom_frame}")
        self.get_logger().info(f"base_frame: {self.base_frame}")

        # Create simulator
        self.get_logger().info("Creating simulator...")
        self.env = gym.make(
            "f110_gym:f110-v0",
            map=self.map_path,
            map_ext=self.map_ext,
            num_agents=1,
            timestep=0.01,
        )
        self.get_logger().info("Simulator created.")

        # Reset simulator
        self._reset_sim()
        self.get_logger().info(f"Observation keys: {list(self.obs.keys())}")




        # 5. Timer
        period = 1.0 / self.scan_rate_hz if self.scan_rate_hz > 0.0 else 0.1
        self.timer = self.create_timer(period, self._on_timer)

    def _reset_sim(self) -> None:
        self.obs, info = self.env.reset(
            options={
                "poses": np.array(
                    [[self.initial_x, self.initial_y, self.initial_theta]],
                    dtype=np.float64,
                )
            }
        )

    def _on_drive(self, msg: AckermannDriveStamped) -> None:
        # Store the latest command so the timer can apply it on the next simulator step.
        self.current_speed = float(msg.drive.speed)
        self.current_steering = float(msg.drive.steering_angle)

        self.get_logger().info(
            f"Received /drive: speed={self.current_speed:.3f}, "
            f"steering={self.current_steering:.3f}"
        )


    def _on_timer(self) -> None:
        action = np.array(
            [[self.current_steering, self.current_speed]],
            dtype=np.float64,
        )

        self.obs, reward, terminated, truncated, info = self.env.step(action)


        
        # if terminated or truncated:
        #     self.get_logger().warn("Episode ended; resetting simulator.")
        #     self._reset_sim()
        #     return
        
        if terminated or truncated:
            self.get_logger().warn("Episode ended; resetting simulator.")
            self._reset_sim()
            return

        # Scan
        scan = np.asarray(self.obs["scans"][0], dtype=np.float32)
        scan = np.nan_to_num(
            scan,
            nan=self.range_max,
            posinf=self.range_max,
            neginf=self.range_min,
        )

        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        msg.angle_min = self.scan_angle_min
        msg.angle_max = self.scan_angle_max
        msg.angle_increment = (msg.angle_max - msg.angle_min) / max(len(scan), 1)
        msg.time_increment = 0.0
        msg.scan_time = 1.0 / self.scan_rate_hz if self.scan_rate_hz > 0.0 else 0.0
        msg.range_min = self.range_min
        msg.range_max = self.range_max
        msg.ranges = scan.tolist()

        self.scan_pub.publish(msg)
        self.get_logger().info("Published /scan")




        # Odometry
        x = float(self.obs["poses_x"][0])
        y = float(self.obs["poses_y"][0])
        theta = float(self.obs["poses_theta"][0])


        vx = float(self.obs["linear_vels_x"][0])
        vy = float(self.obs["linear_vels_y"][0])
        wz = float(self.obs["ang_vels_z"][0])

        qx, qy, qz, qw = Rotation.from_euler("z", theta).as_quat()


        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id = self.base_frame

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = 0.0

        odom.pose.pose.orientation.x = qx
        odom.pose.pose.orientation.y = qy
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = vx
        odom.twist.twist.linear.y = vy
        odom.twist.twist.linear.z = 0.0

        odom.twist.twist.angular.x = 0.0
        odom.twist.twist.angular.y = 0.0
        odom.twist.twist.angular.z = wz

        self.odom_pub.publish(odom)
        self.get_logger().info("Published /odom")

        # TF: odom -> base_link
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = self.odom_frame
        transform.child_frame_id = self.base_frame

        transform.transform.translation.x = x
        transform.transform.translation.y = y
        transform.transform.translation.z = 0.0

        transform.transform.rotation.x = qx
        transform.transform.rotation.y = qy
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(transform)
        self.get_logger().info("Published TF odom -> base_link")

    def _close_sim(self) -> None:
        if hasattr(self, "env") and self.env is not None:
            self.env.close()


def main() -> None:
    rclpy.init()
    node = BridgeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Bridge node interrupted by user.")
    finally:
        node._close_sim()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()