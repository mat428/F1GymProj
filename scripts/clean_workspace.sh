#!/usr/bin/env bash
set -e

docker exec -i f1gym_ros2 bash -lc '
rm -rf /ros2_ws/build /ros2_ws/install /ros2_ws/log
'