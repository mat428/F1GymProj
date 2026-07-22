#!/usr/bin/env python3

from __future__ import annotations

import math
from typing import Tuple
from ..utils.vehicle_state import VehicleState


class PurePursuitController:
    """Pure Pursuit steering controller."""

    def __init__(self, wheelbase: float) -> None:
        self.wheelbase = float(wheelbase)

    def compute_steering(
        self,
        state: VehicleState,
        target_point: Tuple[float, float],
    ) -> float:
        """
        Compute steering angle using Pure Pursuit.

        Args:
            x: Current vehicle x position in odom frame.
            y: Current vehicle y position in odom frame.
            yaw: Current vehicle yaw in odom frame.
            target_point: (x, y) of the lookahead target in odom frame.

        Returns:
            Steering angle in radians.
        """
        tx, ty = target_point

        dx = tx - state.x
        dy = ty - state.y

        # Transform target into vehicle frame
        local_x = math.cos(-state.yaw) * dx - math.sin(-state.yaw) * dy
        local_y = math.sin(-state.yaw) * dx + math.cos(-state.yaw) * dy

        # If the point is behind us, do not steer aggressively toward it
        if local_x <= 0.0:
            return 0.0

        ld2 = local_x * local_x + local_y * local_y
        if ld2 < 1e-6:
            return 0.0

        curvature = 2.0 * local_y / ld2
        steering = math.atan(self.wheelbase * curvature)
        return steering