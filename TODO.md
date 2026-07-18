
# TODO

## Current Sprint

### Stage 4 — Odometry

* [ ] Publish `nav_msgs/Odometry`
* [ ] Test with `ros2 topic echo`
* [ ] Verify RViz
* [ ] Verify timestamps
* [ ] Verify quaternion conversion

---

### Stage 5 — TF

* [ ] Publish `odom → base_link`
* [ ] Verify TF tree
* [ ] Remove temporary static transform

---

### Stage 6 — URDF

* [ ] Robot model
* [ ] Robot State Publisher
* [ ] Display robot in RViz

---

### Stage 7 — Vehicle Control

* [ ] Subscribe to `/drive`
* [ ] Ackermann commands
* [ ] Control simulator

---

### Stage 8 — Complete Bridge

* [ ] Parameter handling
* [ ] Launch files
* [ ] Configuration cleanup
* [ ] Logging
* [ ] Package documentation

---

# Autonomous Driving

## Planning

* [ ] Wall Following
* [ ] Pure Pursuit
* [ ] Stanley
* [ ] MPC

---

## Localization

* [ ] TF
* [ ] EKF
* [ ] Particle Filter

---

## Mapping

* [ ] Occupancy Grid
* [ ] SLAM

---

## AI

* [ ] Reinforcement Learning
* [ ] PPO
* [ ] SAC
* [ ] Imitation Learning

---

## Vision

* [ ] Camera interface
* [ ] Object detection
* [ ] Lane detection

---

## Digital Twin

* [ ] Cloud communication
* [ ] Remote monitoring
* [ ] Data logging
* [ ] Real vehicle synchronization

---

# Repository Improvements

* [ ] Clean Dockerfile
* [ ] Version pinning
* [ ] GitHub Actions
* [ ] Automatic environment setup
* [ ] Development documentation
* [ ] Release v0.1.0
