# The F1TENTH Gym environment

This is the repository of the F1TENTH Gym environment.

You can find the [documentation](https://f1tenth-gym.readthedocs.io/en/latest/) of the environment here.

## Quickstart

**Requirements:** Python 3.10 - 3.12

Install the environment:

```bash
git clone https://github.com/PARKasd/f1tenth_gym.git
cd f1tenth_gym
pip install -e .
```

If you hit a numba/coverage error (`AttributeError: module 'coverage.types' has no attribute 'Tracer'`):
```bash
pip install "coverage>=7.6"
```

If you hit a setuptools error (`pkgutil.ImpImporter`):
```bash
pip install --upgrade setuptools
```

Run the waypoint follow example:
```bash
cd examples
python3 waypoint_follow.py
```

## Usage

```python
import gymnasium as gym
import numpy as np

env = gym.make('f110_gym:f110-v0',
               map='vegas',
               map_ext='.png',
               num_agents=1,
               timestep=0.01)

obs, info = env.reset(options={'poses': np.array([[0.0, 0.0, 0.0]])})

while True:
    action = np.array([[0.0, 2.0]])  # [steering_angle, velocity]
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()
    if terminated or truncated:
        break
```

### Available maps
`berlin`, `vegas`, `skirk`, `levine`, `stata_basement`, or an absolute path to a custom map YAML file.

### Observation keys
`ego_idx`, `scans`, `poses_x`, `poses_y`, `poses_theta`, `linear_vels_x`, `linear_vels_y`, `ang_vels_z`, `collisions`, `lap_times`, `lap_counts`

### Action format
`np.ndarray(num_agents, 2)` — each row is `[steering_angle, velocity]`

## ROS 2 Integration (Jazzy Jalisco)

For ROS 2 Jazzy Jalisco, see [f1tenth_gym_ros_jazzy](https://github.com/PARKasd/f1tenth_gym_ros_jazzy).

### Prerequisites

1. Install f1tenth_gym first (see Quickstart above).

2. Install Python dependencies:
```bash
pip install transforms3d
```

3. Install ROS 2 dependencies:
```bash
sudo apt install ros-jazzy-nav2-map-server \
                 ros-jazzy-nav2-lifecycle-manager \
                 ros-jazzy-ackermann-msgs \
                 ros-jazzy-xacro \
                 ros-jazzy-joint-state-publisher \
                 ros-jazzy-teleop-twist-keyboard
```

4. If you are on an Ubuntu derivative (e.g. HamoniKR, Pop!_OS, Mint) and rosdep fails with `Could not detect OS`, set:
```bash
export ROS_OS_OVERRIDE=ubuntu:noble  # for 24.04-based distros
echo 'export ROS_OS_OVERRIDE=ubuntu:noble' >> ~/.bashrc  # or ~/.zshrc
```

### Build and launch

```bash
# Clone into your workspace
cd ~/sim_ws/src
git clone https://github.com/PARKasd/f1tenth_gym_ros_jazzy.git f1tenth_gym_ros

# Build
cd ~/sim_ws
colcon build --packages-select f1tenth_gym_ros
source install/setup.bash  # or setup.zsh

# Launch
ros2 launch f1tenth_gym_ros gym_bridge_launch.py
```

## Docker

A Dockerfile is provided with GUI support (nvidia GPU required):
```bash
docker build -t f1tenth_gym_container -f Dockerfile .
docker run --gpus all -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix f1tenth_gym_container
```

## Citing
If you find this Gym environment useful, please consider citing:

```
@inproceedings{okelly2020f1tenth,
  title={F1TENTH: An Open-source Evaluation Environment for Continuous Control and Reinforcement Learning},
  author={O'Kelly, Matthew and Zheng, Hongrui and Karthik, Dhruv and Mangharam, Rahul},
  booktitle={NeurIPS 2019 Competition and Demonstration Track},
  pages={77--89},
  year={2020},
  organization={PMLR}
}
```
