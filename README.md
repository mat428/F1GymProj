
# F1TENTH ROS 2 Jazzy Bridge

## Overview

This project develops a custom ROS 2 Jazzy bridge for the latest F1TENTH Gym simulator. Rather than relying on an existing bridge, the goal is to build every component from scratch and understand how ROS 2, DDS, RViz, TF, and the simulator interact.

The bridge converts simulator observations into standard ROS 2 messages that can later be consumed by planners, controllers, localization systems, SLAM, reinforcement learning algorithms, and ultimately a physical F1TENTH vehicle.

This project also serves as the software foundation for future Digital Twin research.

---

# Objectives

* Learn ROS 2 at a professional level.
* Build a complete simulator bridge.
* Understand DDS communication.
* Publish standard ROS interfaces.
* Support future planners and controllers.
* Prepare for Digital Twin integration.

---

# Current Features

* ROS 2 Jazzy package
* F1TENTH Gym integration
* LaserScan publisher
* RViz visualization
* Docker-based development
* Unified Python environment
* Configuration files
* Launch files

Current implementation:

```text
F1TENTH Gym
      │
Observation Dictionary
      │
Bridge Node
      │
 ├────────────┐
 │            │
 ▼            ▼
/scan     (next: /odom)
```

---

# Project Structure

```text
F1GymProj/
│
├── README.md
├── NOTES.md
├── TODO.md
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── ros2_ws/
│
└── simulator/
```

Inside Docker:

```text
/sim_ws
```

---

# Docker Environment

The development environment contains

* ROS 2 Jazzy
* Python virtual environment (`/opt/venv`)
* Colcon
* F1TENTH Gym
* Bridge package

---

# ROS Topics

Implemented

| Topic | Type                  |
| ----- | --------------------- |
| /scan | sensor_msgs/LaserScan |

Planned

* /odom
* /tf
* /drive

---

# Build

```bash
cd /sim_ws
colcon build --symlink-install
source install/setup.bash
```

---

# Run

```bash
ros2 run my_f1tenth_bridge bridge_node
```

---

# Roadmap

## Phase 1 — Bridge

* ROS package
* Simulator
* LaserScan
* Odometry
* TF
* URDF
* Robot Model
* Ackermann Drive
* Complete bridge

## Phase 2 — Autonomous Driving

* Wall Following
* Pure Pursuit
* Stanley
* MPC
* Localization
* SLAM

## Phase 3 — AI

* Reinforcement Learning
* Imitation Learning
* Vision
* Digital Twin
* Physical F1TENTH

---

# License

MIT
