#!/usr/bin/env bash
set -e

docker exec -it f1gym_ros2 bash -c "
cd /sim_ws
rm -rf build install log
"