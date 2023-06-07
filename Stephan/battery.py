import numpy as np
import time


class Battery:
    def __init__(self, px_coordinates: tuple, mm_coordinates: tuple, zone: str, rotation: int, marker_contour: np.ndarray, placed_to_charger_time: float = 0.0) -> None:
        self.px_coordinates = px_coordinates
        self.mm_coordinates = mm_coordinates
        self.rotation_degree = rotation
        self.zone = zone  # Zones: battery_charged, robot_left, robot_right, battery_discharged
        self.marker_controur = marker_contour
        self.detected_time = time.time()
        self.placed_to_charger_time = placed_to_charger_time

    def __str__(self) -> str:
        return f"Battery in {self.zone} zone; MM Coords: {self.mm_coordinates}"
