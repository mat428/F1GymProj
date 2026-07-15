
# Hand Servo ROS 2

A complete ROS 2 and Docker project that controls a physical servo motor connected to an Arduino Uno while simultaneously visualizing the servo motion as a digital twin in RViz.

The project demonstrates how a single ROS topic can control both a real robot component and its virtual representation.

---

# Features

- ROS 2 Jazzy
- Docker-based development environment
- Arduino Uno serial communication
- Servo motor control
- RViz digital twin
- Tkinter GUI slider
- URDF robot model
- Robot State Publisher
- Joint State Publisher
- Clean ROS topic architecture

---

# Project Architecture

```
                 +----------------------+
                 |  Servo Slider GUI    |
                 |  publishes Int32     |
                 +----------+-----------+
                            |
                     /servo_angle
                            |
             +--------------+--------------+
             |                             |
             |                             |
             ▼                             ▼
     Servo Bridge Node          Servo Joint State Node
      (USB Serial)              (/joint_states)
             |                             |
             ▼                             ▼
        Arduino Uno             Robot State Publisher
             |                             |
             ▼                             ▼
        Physical Servo                  RViz
```

---

# Hardware Requirements

- Arduino Uno
- Servo Motor
- USB Cable
- Ubuntu 26.04
- Docker
- Docker Compose

---

# Software Requirements

- ROS 2 Jazzy
- Docker
- Docker Compose
- RViz2
- Python 3
- Tkinter

---

# Folder Structure

```
hand-servo-ros2/
│
├── README.md
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── arduino/
│   └── servo_driver.ino
│
└── ros2_ws/
    └── src/
        └── servo_bridge/
            ├── launch/
            ├── urdf/
            ├── servo_bridge/
            ├── package.xml
            └── setup.py
```

---

# Arduino Wiring

| Servo Wire | Arduino Uno                |
| ---------- | -------------------------- |
| Signal     | D9                         |
| VCC        | 5V (or external 5V supply) |
| GND        | GND                        |

For larger servos, use an external regulated 5V power supply and connect the power supply GND to the Arduino GND.

---

# Building the Project

Clone the repository:

```bash
git clone https://github.com/mat428/slider-servo-ros2-docker.git

cd slider-servo-ros2-docker
```

Build the Docker image:

```bash
cd docker

docker compose build
```

---

# Starting the Project

Allow Docker to display GUI applications:

```bash
xhost +local:docker
```

Start the Docker container:

```bash
docker compose up -d
```

---

# Terminal 1 — Start ROS, Arduino Bridge and RViz

```bash
cd docker

docker compose exec ros2 bash

source /opt/ros/jazzy/setup.bash

cd /workspace/ros2_ws

colcon build

source install/setup.bash

ros2 launch servo_bridge servo_rviz.launch.py port:=/dev/ttyACM0
```

---

# Terminal 2 — Start the GUI Slider

```bash
cd docker

docker compose exec ros2 bash

source /opt/ros/jazzy/setup.bash

cd /workspace/ros2_ws

source install/setup.bash

ros2 run servo_bridge servo_slider_gui
```

Move the slider to control:

- the physical servo
- the RViz digital twin

simultaneously.

---

# ROS Topics

## Published

```
/servo_angle
```

Type

```
std_msgs/msg/Int32
```

---

## Published

```
/joint_states
```

Type

```
sensor_msgs/msg/JointState
```

---

# ROS Nodes

```
servo_slider_gui
```

Publishes servo angles from the GUI.

---

```
servo_bridge_node
```

Receives servo angles and sends them to the Arduino over USB Serial.

---

```
servo_joint_state_node
```

Converts servo angles into JointState messages for RViz.

---

```
robot_state_publisher
```

Computes the TF tree from the URDF.

---

```
rviz2
```

Displays the digital twin.

---

# Digital Twin

The digital twin is implemented using:

- URDF
- JointState messages
- Robot State Publisher
- RViz

The virtual servo follows exactly the same ROS topic as the physical servo.

---

# Troubleshooting

## Arduino not found

Check:

```bash
ls /dev/ttyACM*
```

If the port is different, change the launch argument:

```bash
ros2 launch servo_bridge servo_rviz.launch.py port:=/dev/ttyUSB0
```

---

## Servo does not move

Check:

- Arduino sketch uploaded
- Correct wiring
- Servo powered correctly
- USB cable connected
- No other application is using `/dev/ttyACM0`

---

## RViz shows TF errors

Verify:

- Fixed Frame is set to `world`
- RobotModel display is enabled
- TF display is enabled

---

## Docker GUI does not appear

Run:

```bash
xhost +local:docker
```

before starting Docker.

---

# Technologies Used

- ROS 2 Jazzy
- Docker
- Python
- Tkinter
- RViz2
- URDF
- Robot State Publisher
- Arduino Uno
- Serial Communication

---

# Learning Objectives

This project demonstrates:

- ROS 2 node development
- Topic-based communication
- Dockerized robotics development
- Serial communication with Arduino
- Hardware abstraction
- Robot visualization
- Digital Twin concepts
- URDF modeling
- RViz visualization

---

# Future Improvements

- RealSense D435i hand tracking
- MediaPipe hand detection
- Gesture recognition
- PID servo control
- Servo feedback
- ROS 2 Actions
- Launch all components with a single command

---

# License

MIT License

---

# Author

**Matin Afshari**

Tallinn University of Technology (TalTech)

Robotics and Autonomous Systems
