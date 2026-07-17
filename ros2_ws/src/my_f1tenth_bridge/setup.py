from setuptools import find_packages, setup

package_name = "my_f1tenth_bridge"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", ["launch/bridge.launch.py"]),
        (f"share/{package_name}/config", ["config/sim.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Matin",
    maintainer_email="matin42854@email.com",
    description="Custom F1TENTH bridge package for ROS 2 Jazzy",
    license="MIT",
    entry_points={
        "console_scripts": [
            "bridge_node = my_f1tenth_bridge.bridge_node:main",
        ],
    },
)