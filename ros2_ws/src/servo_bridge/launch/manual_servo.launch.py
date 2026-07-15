
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'port',
            default_value='/dev/ttyACM0',
            description='Arduino serial port',
        ),
        DeclareLaunchArgument(
            'baudrate',
            default_value='115200',
            description='Serial baud rate',
        ),
        DeclareLaunchArgument(
            'topic_name',
            default_value='/servo_angle',
            description='ROS topic for servo angles',
        ),
        Node(
            package='servo_bridge',
            executable='manual_servo_node',
            name='servo_bridge_node',
            output='screen',
            parameters=[{
                'port': LaunchConfiguration('port'),
                'baudrate': LaunchConfiguration('baudrate'),
                'topic_name': LaunchConfiguration('topic_name'),
            }],
        ),
    ])
