#!/usr/bin/env bash
set -e

docker exec -i f1gym_ros2 bash -lc '
source /opt/ros/jazzy/setup.bash
source /opt/venv/bin/activate
cd /ros2_ws
colcon build --symlink-install
'