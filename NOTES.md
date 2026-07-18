
# Development Notes

This file records important engineering decisions, debugging sessions, architectural choices, and lessons learned during development.

---

# Environment

Host

* Ubuntu VM
* Docker
* RViz
* VS Code
* Git

Container

* ROS 2 Jazzy
* Python virtual environment
* F1TENTH Gym
* Colcon
* Bridge package

---

# DDS Communication

Initial issue:

Topics were discovered but LaserScan messages were not received on the host.

Solution:

```text
FASTDDS_BUILTIN_TRANSPORTS=UDPv4
```

Docker:

```yaml
network_mode: host
ipc: host
```

Host:

```bash
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
```

---

# Python Environment

The project uses

```text
/opt/venv
```

for all simulator and bridge dependencies.

Important lesson:

Avoid mixing

```text
/usr/bin/python3
```

and

```text
/opt/venv/bin/python3
```

inside the same ROS workspace.

A single Python environment prevents package conflicts and simplifies maintenance.

---

# RViz

Current configuration

Fixed Frame

```text
laser
```

LaserScan

* Best Effort
* Volatile
* Points
* 5 px

---

# Completed Stages

✓ ROS package

✓ Simulator integration

✓ LaserScan publishing

✓ RViz visualization

✓ DDS networking

✓ Unified Python environment

---

# Useful Commands

Build

```bash
colcon build --symlink-install
```

Source

```bash
source install/setup.bash
```

Run bridge

```bash
ros2 run my_f1tenth_bridge bridge_node
```

Check topics

```bash
ros2 topic list
```

Echo scan

```bash
ros2 topic echo /scan --once --qos-profile sensor_data
```

---

# Lessons Learned

* Build incrementally.
* Test after every feature.
* Keep ROS topics standard.
* Separate simulator logic from ROS interface when possible.
* Keep Docker reproducible.
* Document every architecture decision.

---

# Future Improvements

* Automatic Docker startup
* Version pinning
* CI build
* GitHub Actions
* Documentation website
* Unit tests
* Integration tests
