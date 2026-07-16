FROM osrf/ros:jazzy-desktop

RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*


SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc
WORKDIR /workspace

CMD ["bash"]