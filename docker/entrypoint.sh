#!/usr/bin/env bash

set -e

echo ""
echo "==============================================="
echo "      F1TENTH ROS 2 Development Container"
echo "==============================================="
echo ""

# ROS 2
source /opt/ros/jazzy/setup.bash

# Python environment
source /opt/venv/bin/activate

# Workspace overlay (if it exists)
if [ -f /sim_ws/install/setup.bash ]; then
    source /sim_ws/install/setup.bash
fi

cd /sim_ws

exec "$@"