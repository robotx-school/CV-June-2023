from typing import List


class Robot:
    def __init__(self, zone: str, bounding_rect: List[tuple], battery: object = None) -> None:
        self.bounding_rect_px = bounding_rect
        self.statis_frames_count = 0
        self.zone = zone
        self.battery = battery
        self.center = self.get_center()

    def get_center(self) -> dict:
        x1, y1 = self.bounding_rect_px[0]
        x4, y4 = self.bounding_rect_px[-1]
        x = (x1 + x4) / 2
        y = (y1 + y4) / 2
        return (x, y)

    def is_static(self) -> bool:
        return self.statis_frames_count > 5

    def __str__(self) -> str:
        return f"Robot in zone: {self.zone}; center: {self.get_center()}; static: {self.is_static()}"
