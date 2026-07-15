import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('servo_bridge')
    urdf_path = os.path.join(pkg_share, 'urdf', 'servo_demo.urdf')

    with open(urdf_path, 'r') as inf:
        robot_description = inf.read()

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

        Node(
            package='servo_bridge',
            executable='servo_bridge_node',
            name='servo_bridge_node',
            output='screen',
            parameters=[{
                'port': LaunchConfiguration('port'),
                'baudrate': LaunchConfiguration('baudrate'),
            }],
        ),

        Node(
            package='servo_bridge',
            executable='servo_joint_state_node',
            name='servo_joint_state_node',
            output='screen',
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
            }],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        ),
    ])