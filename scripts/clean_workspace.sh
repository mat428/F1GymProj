#!/usr/bin/env bash
set -e

docker exec -it f1gym_ros2 bash -c "
cd /ros2_ws
rm -rf build install log
"