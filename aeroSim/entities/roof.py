from aeroSim.entities.obstacle import Obstacle
import math

class Roof(Obstacle):
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        dx = x2 - x1
        dy = y2 - y1
        self.length = math.sqrt(dx * dx + dy * dy)

        if self.length > 0:
            self.dir_x = dx / self.length
            self.dir_y = dy / self.length
            self.normal_x = -self.dir_y
            self.normal_y = self.dir_x
        else:
            self.dir_x = 1.0
            self.dir_y = 0.0
            self.normal_x = 0.0
            self.normal_y = 1.0

    def get_closest_point(self, px: float, py: float) -> tuple[float, float]:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1

        if self.length == 0:
            return self.x1, self.y1

        t = ((px - self.x1) * dx + (py - self.y1) * dy) / (self.length * self.length)
        t = max(0.0, min(1.0, t))

        closest_x = self.x1 + t * dx
        closest_y = self.y1 + t * dy
        return closest_x, closest_y

    def get_corners(self) -> list[tuple[float, float]]:
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def contains(self, px: float, py: float) -> bool:
        return False