import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from sensor_msgs.msg import JointState


class ServoJointStateNode(Node):
    def __init__(self):
        super().__init__('servo_joint_state_node')

        self.subscription = self.create_subscription(
            Int32,
            '/servo_angle',
            self.angle_callback,
            10
        )

        self.publisher = self.create_publisher(JointState, '/joint_states', 10)

        self.get_logger().info('Listening to /servo_angle and publishing /joint_states')

    def angle_callback(self, msg):
        angle_deg = max(0, min(180, int(msg.data)))
        angle_rad = math.radians(angle_deg)

        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['servo_joint']
        joint_state.position = [angle_rad]

        self.publisher.publish(joint_state)
        self.get_logger().info(f'Published joint state: {angle_deg} deg')


def main():
    rclpy.init()
    node = ServoJointStateNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()