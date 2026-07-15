ARG ROS_DISTRO=jazzy
FROM ros:${ROS_DISTRO}-ros-base

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-serial \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-tk \
    ros-jazzy-rviz2 \
    git \
    usbutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN rosdep init || true && rosdep update || true

CMD ["bash"]
