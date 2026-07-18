#!/usr/bin/env python3

from __future__ import annotations

import numpy as np
import gymnasium as gym
import f110_gym  # registers the f110_gym environment
import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSDurabilityPolicy,
    QoSProfile,
    QoSReliabilityPolicy,
)
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from scipy.spatial.transform import Rotation



class BridgeNode(Node):
    def __init__(self) -> None:
        super().__init__("bridge")

        # Parameters
        self.declare_parameter("map_path", "/sim_ws/src/my_f1tenth_bridge/assets/maps/levine")
        self.declare_parameter("scan_topic", "/scan")
        self.declare_parameter("odom_topic", "/odom")
        self.declare_parameter("drive_topic", "/drive")
        self.declare_parameter("frame_id", "laser")

        self.map_path = self.get_parameter("map_path").value
        self.scan_topic = self.get_parameter("scan_topic").value
        self.odom_topic = self.get_parameter("odom_topic").value
        self.drive_topic = self.get_parameter("drive_topic").value
        self.frame_id = self.get_parameter("frame_id").value

        # QoS for sensor data
        scan_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
        )
        self.scan_pub = self.create_publisher(LaserScan, self.scan_topic, scan_qos)
        self.odom_pub = self.create_publisher(Odometry, "/odom", 10)



        self.get_logger().info("Bridge node started.")
        self.get_logger().info(f"map_path: {self.map_path}")
        self.get_logger().info(f"scan_topic: {self.scan_topic}")
        self.get_logger().info(f"odom_topic: {self.odom_topic}")
        self.get_logger().info(f"drive_topic: {self.drive_topic}")
        self.get_logger().info(f"frame_id: {self.frame_id}")

        # Create simulator
        self.get_logger().info("Creating simulator...")
        self.env = gym.make(
            "f110_gym:f110-v0",
            map=self.map_path,
            map_ext=".png",
            num_agents=1,
            timestep=0.01,
        )
        self.get_logger().info("Simulator created.")

        # Reset simulator
        self.obs, info = self.env.reset(
            options={"poses": np.array([[0.0, 0.0, 0.0]])}
        )
        self.get_logger().info("Simulator reset.")
        self.get_logger().info(f"Observation keys: {list(self.obs.keys())}")

        # Temporary timer to step simulator and publish scan
        self.timer = self.create_timer(0.1, self._on_timer)

    def _on_timer(self) -> None:
        action = np.array([[0.0, 0.0]])

        self.obs, reward, terminated, truncated, info = self.env.step(action)
        
        #SCAN:
        scan = self.obs["scans"][0]

        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id

        msg.angle_min = -2.35
        msg.angle_max = 2.35
        msg.angle_increment = (msg.angle_max - msg.angle_min) / len(scan)
        msg.range_min = 0.0
        msg.range_max = 30.0
        msg.ranges = scan.tolist()

        self.scan_pub.publish(msg)
        self.get_logger().info("Published /scan")

        #ODOM:
        # Extract simulator state
        x = float(self.obs["poses_x"][0])
        y = float(self.obs["poses_y"][0])
        theta = float(self.obs["poses_theta"][0])

        vx = float(self.obs["linear_vels_x"][0])
        vy = float(self.obs["linear_vels_y"][0])
        wz = float(self.obs["ang_vels_z"][0])

        # Convert yaw to quaternion
        quat = Rotation.from_euler("z", theta).as_quat()
        qx, qy, qz, qw = quat

        # Build Odometry message
        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

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

def main() -> None:
    rclpy.init()
    node = BridgeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Bridge node interrupted by user.")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()