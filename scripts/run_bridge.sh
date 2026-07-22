#!/usr/bin/env bash
set -e

docker exec -it f1gym_ros2 bash -lc '
source /opt/ros/jazzy/setup.bash
source /opt/venv/bin/activate
cd /ros2_ws
source install/setup.bash
ros2 launch my_f1tenth_bridge bridge.launch.py
'