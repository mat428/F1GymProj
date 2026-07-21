from setuptools import find_packages, setup
from glob import glob
import os

package_name = "my_f1tenth_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),

    data_files=[
        # Register the package with the ROS 2 package index.
        (
            "share/ament_index/resource_index/packages",
            [f"resource/{package_name}"],
        ),

        # Install package.xml into the package share directory.
        (
            f"share/{package_name}",
            [
                "package.xml",
            ],
        ),

        # Install launch files so they are available after colcon build.
        (
            f"share/{package_name}/launch",
            glob("launch/*.py"),
        ),

        # Install configuration files.
        (
            f"share/{package_name}/config",
            glob("config/*"),
        ),

        # Install URDF/Xacro assets so robot_state_publisher can load them.
        (
            f"share/{package_name}/assets/urdf",
            glob("assets/urdf/*"),
        ),

        # Install any planner path files or other plain text assets later if needed.
    ],

    install_requires=[
        "setuptools",
    ],

    zip_safe=False,

    maintainer="Matin Afshari",
    maintainer_email="matin42854@email.com",

    description=(
        "Custom ROS 2 Jazzy bridge for the F1TENTH Gym simulator."
    ),

    license="MIT",

    keywords=[
        "ROS2",
        "F1TENTH",
        "simulation",
        "robotics",
        "autonomous driving",
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Robotics",
    ],

    entry_points={
        "console_scripts": [
            # Main simulator bridge node.
            "bridge_node = my_f1tenth_bridge.bridge_node:main",

            # Pure Pursuit planner node.
            "pure_pursuit_planner = my_f1tenth_bridge.planner_node:main",
        ],
    },
)