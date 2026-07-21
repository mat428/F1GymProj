#!/usr/bin/env bash
set -e

docker exec -it f1gym_ros2 bash -c "
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 run my_f1tenth_bridge bridge_node
"