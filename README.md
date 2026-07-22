# F1TENTH ROS 2 Bridge

A modular ROS 2 Jazzy bridge for the F1TENTH Gym simulator.

The project provides a clean architecture for autonomous driving development, where the simulator, ROS 2 bridge, controllers, planners, and utilities are separated into independent modules.

---

# Current Features

## Simulator Bridge

- ROS 2 Jazzy
- F1TENTH Gym integration
- Ackermann drive interface
- LaserScan publisher
- Odometry publisher
- TF broadcaster
- Robot State Publisher
- URDF visualization

Published topics

- /scan
- /odom
- /tf

Subscribed topics

- /drive

---

## Planner

Current controller

- Pure Pursuit

Architecture

Planner
↓
WaypointManager
↓
PurePursuitController
↓
Ackermann Drive

---

## Waypoints

Waypoints are stored as CSV files.

Example

```
assets/waypoints/
    levine_centerline.csv
```

The planner no longer contains hardcoded waypoint lists.

---

## Project Structure

```
F1GymProj
│
├── docker
├── simulator
├── ros2_ws
│
└── src
    └── my_f1tenth_bridge
        │
        ├── launch
        ├── config
        ├── assets
        ├── urdf
        │
        └── my_f1tenth_bridge
            ├── bridge_node.py
            ├── planner_node.py
            │
            ├── controllers
            │     ├── pure_pursuit.py
            │     ├── stanley.py
            │     └── mpc.py
            │
            ├── planners
            │     ├── waypoint_manager.py
            │     ├── astar.py
            │     ├── hybrid_astar.py
            │     └── rrt.py
            │
            ├── localization
            │
            ├── perception
            │
            └── utils
```

---

# Running

Inside Docker

```
cd /ros2_ws

colcon build --symlink-install

source install/setup.bash

ros2 launch my_f1tenth_bridge bridge.launch.py
```

RViz runs on the host machine.

---

# Current Architecture

VehicleState

↓

WaypointManager

↓

PurePursuitController

↓

Planner Node

↓

Bridge Node

↓

F1TENTH Gym

---

# Development Roadmap

Completed

- Simulator bridge
- LaserScan
- Odometry
- TF
- URDF
- Pure Pursuit
- Waypoint CSV loading
- VehicleState abstraction

Next

- Stanley Controller
- MPC Controller
- Occupancy Grid Mapping
- A*
- Hybrid A*
- RRT
- Particle Filter
- EKF
- SLAM
- Digital Twin
- Autoware integration
