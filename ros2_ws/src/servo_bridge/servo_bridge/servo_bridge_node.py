
import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class ServoBridgeNode(Node):
    def __init__(self):
        super().__init__('servo_bridge_node')

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('topic_name', '/servo_angle')

        port = self.get_parameter('port').value
        baudrate = int(self.get_parameter('baudrate').value)
        topic_name = self.get_parameter('topic_name').value

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.get_logger().info(f'Connected to Arduino on {port} at {baudrate}')
        except Exception as exc:
            self.get_logger().error(f'Could not open serial port {port}: {exc}')
            raise

        self.subscription = self.create_subscription(
            Int32,
            topic_name,
            self.angle_callback,
            10
        )

        self.get_logger().info(f'Subscribed to {topic_name}')

    def angle_callback(self, msg):
        angle = int(msg.data)
        angle = max(0, min(180, angle))
        self.ser.write(f'{angle}\n'.encode('utf-8'))
        self.get_logger().info(f'Sent angle: {angle}')

    def close(self):
        if hasattr(self, 'ser') and self.ser and self.ser.is_open:
            self.ser.close()
            self.get_logger().info('Serial connection closed')


def main():
    rclpy.init()
    node = None

    try:
        node = ServoBridgeNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.close()
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()