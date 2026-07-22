from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

from ament_index_python.packages import get_package_share_directory
import os
import xacro


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    config_file = LaunchConfiguration("config_file")

    default_config = PathJoinSubstitution(
        [FindPackageShare("my_f1tenth_bridge"), "config", "sim.yaml"]
    )

    urdf_path = os.path.join(
        get_package_share_directory("my_f1tenth_bridge"),
        "urdf",
        "racecar.urdf.xacro",
    )
    robot_description = xacro.process_file(urdf_path).toxml()

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulated clock if true",
            ),
            DeclareLaunchArgument(
                "config_file",
                default_value=default_config,
                description="Path to the bridge parameter file",
            ),
            Node(
                package="my_f1tenth_bridge",
                executable="bridge_node",
                name="bridge",
                output="screen",
                parameters=[
                    config_file,
                    {"use_sim_time": use_sim_time},
                ],
            ),

            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time},
                ],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time},
                    {"robot_description": robot_description},
                ],
            ),

            # Pure Pursuit planner
            Node(
                package="my_f1tenth_bridge",
                executable="pure_pursuit_planner",
                name="pure_pursuit_planner",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": use_sim_time,
                        "odom_topic": "/odom",
                        "drive_topic": "/drive",
                        "lookahead_distance": 1.5,
                        "target_speed": 0.6,
                        "wheelbase": 0.3302,
                        "control_rate_hz": 20.0,
                        # "waypoints_flat": [
                        #     0.5, 0.5,
                        #     1.5, 0.5,
                        #     2.5, -0.5,
                        #     3.5, -0.5,
                        #     4.5, -0.5,
                        #     5.5, 0.5,
                        #     6.5, 0.5,
                        #     7.5, -0.5,
                        #     8.5, -0.5,
                        #     9.5, 0.5,
                        # ],
                    },
                ],
            ),

        ]
    )