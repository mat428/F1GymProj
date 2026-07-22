
# Project Notes

## Current Status

The bridge is fully operational.

ROS 2 ↔ F1TENTH Gym communication works.

Published

- LaserScan
- Odometry
- TF

Subscribed

- Ackermann Drive

RViz visualization is operational.

---

## Software Architecture

Planner Node

Responsible for

- ROS interfaces
- planner orchestration
- publishing drive commands

No controller mathematics should remain here.

---

PurePursuitController

Responsible for

- steering computation only

No ROS code.

---

WaypointManager

Responsible for

- loading CSV files
- waypoint search
- waypoint reset
- end-of-path detection

No ROS code.

---

VehicleState

Stores

- x
- y
- yaw
- speed
- yaw_rate

Used by all future planners and controllers.

---

Bridge Node

Responsible for

- simulator
- LaserScan
- Odometry
- TF
- Ackermann commands

No planning algorithms.

---

## Design Rules

Controllers never publish ROS topics.

WaypointManager never publishes ROS topics.

Bridge never computes steering.

Planner never performs simulator communication.

Utilities never depend on ROS.

---

## Coding Style

- Small classes
- Single responsibility
- Type hints everywhere
- Minimal logging
- Parameters from configuration files
- CSV for paths
- Future algorithms should plug into the same interfaces

---

## Next Tasks

High priority

- Stanley Controller
- MPC Controller

Medium priority

- Occupancy Grid
- A*

Future

- Hybrid A*
- RRT
- EKF
- Particle Filter
- SLAM
- Digital Twin
- Autoware
