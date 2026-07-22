from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import List, Tuple


class WaypointManager:

    def __init__(self) -> None:
        self.waypoints: List[Tuple[float, float]] = []
        self.current_waypoint_index = 0

    def load_from_csv(self, filename: str) -> None:
        self.waypoints.clear()

        with open(Path(filename), newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.waypoints.append(
                    (
                        float(row["x"]),
                        float(row["y"]),
                    )
                )

        self.current_waypoint_index = 0

    def reset(self) -> None:
        self.current_waypoint_index = 0

    def get_lookahead_point(
        self,
        x: float,
        y: float,
        lookahead_distance: float,
    ) -> Tuple[float, float] | None:

        if not self.waypoints:
            return None

        for i in range(
            self.current_waypoint_index,
            len(self.waypoints),
        ):

            wx, wy = self.waypoints[i]

            dist = math.hypot(
                wx - x,
                wy - y,
            )

            if dist >= lookahead_distance:
                self.current_waypoint_index = i
                return wx, wy

        self.current_waypoint_index = len(self.waypoints) - 1
        return self.waypoints[-1]