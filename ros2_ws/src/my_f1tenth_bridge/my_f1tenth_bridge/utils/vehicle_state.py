from dataclasses import dataclass


@dataclass
class VehicleState:
    """
    Current state of the vehicle in the odom frame.
    """

    x: float = 0.0
    y: float = 0.0
    yaw: float = 0.0

    speed: float = 0.0

    yaw_rate: float = 0.0