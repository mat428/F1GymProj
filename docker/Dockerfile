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
    ros-jazzy-ackermann-msgs \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-nav2-lifecycle-manager \
    ros-jazzy-nav2-map-server \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-xacro \
    ros-jazzy-tf-transformations \
 && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true && rosdep update || true

RUN python3 -m venv --system-site-packages /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip wheel "setuptools<80"

RUN pip install --ignore-installed \
    colcon-core \
    colcon-common-extensions

COPY docker/requirements-bridge.txt /tmp/requirements-bridge.txt
RUN pip install --no-cache-dir -r /tmp/requirements-bridge.txt

COPY simulator/f1tenth_gym /opt/f1tenth_gym
RUN pip install --no-cache-dir -e /opt/f1tenth_gym

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc
RUN echo "source /opt/venv/bin/activate" >> /root/.bashrc
COPY docker/entrypoint.sh /opt/entrypoint.sh

RUN chmod +x /opt/entrypoint.sh

ENTRYPOINT ["/opt/entrypoint.sh"]

WORKDIR /ros2_ws

CMD ["bash"]
