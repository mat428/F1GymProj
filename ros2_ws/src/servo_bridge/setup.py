from setuptools import setup

package_name = 'servo_bridge'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/manual_servo.launch.py',
            'launch/servo_rviz.launch.py',
        ]),
        ('share/' + package_name + '/urdf', [
            'urdf/servo_demo.urdf',
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Matin Afshari',
    maintainer_email='hosein.afshari@taltech.ee',
    description='ROS 2 bridge between laptop and Arduino servo',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'servo_bridge_node = servo_bridge.servo_bridge_node:main',
            'servo_slider_gui = servo_bridge.servo_slider_gui:main',
            'servo_joint_state_node = servo_bridge.servo_joint_state_node:main',
            'manual_servo_node = servo_bridge.servo_bridge_node:main',
        ],
    },
)