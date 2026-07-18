from setuptools import find_packages, setup

package_name = "my_f1tenth_bridge"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),

    data_files=[
        (
            "share/ament_index/resource_index/packages",
            [f"resource/{package_name}"],
        ),
        (
            f"share/{package_name}",
            [
                "package.xml",
            ],
        ),
        (
            f"share/{package_name}/launch",
            [
                "launch/bridge.launch.py",
            ],
        ),
        (
            f"share/{package_name}/config",
            [
                "config/sim.yaml",
            ],
        ),
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
            "bridge_node = my_f1tenth_bridge.bridge_node:main",
        ],
    },
)