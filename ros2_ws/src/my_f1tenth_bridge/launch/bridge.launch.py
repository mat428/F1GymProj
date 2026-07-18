from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    config_file = LaunchConfiguration("config_file")

    default_config = PathJoinSubstitution(
        [FindPackageShare("my_f1tenth_bridge"), "config", "sim.yaml"]
    )

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
        ]
    )