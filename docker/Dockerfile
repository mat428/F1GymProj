FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy
ENV ROS_DOMAIN_ID=0
ENV ROS_LOCALHOST_ONLY=0

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    nano \
    vim \
    python3-pip \
    python3-venv \
    python3-rosdep \
    python3-colcon-common-extensions \
    ros-jazzy-ackermann-msgs \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-nav2-lifecycle-manager \
    ros-jazzy-nav2-map-server \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-xacro \
 && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true && rosdep update || true

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc
RUN echo "source /opt/venv/bin/activate" >> /root/.bashrc

WORKDIR /sim_ws
CMD ["bash"]