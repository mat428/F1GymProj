#!/usr/bin/env bash
set -e

docker exec -it f1gym_ros2 bash -c "colcon build --symlink-install"