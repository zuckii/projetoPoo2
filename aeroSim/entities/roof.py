from aeroSim.entities.obstacle import Obstacle
import math

class Roof(Obstacle):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, rotation_speed: float = 0.0) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.rotation_speed = rotation_speed
        self.angle = 0.0
        
        self.cx = (x1 + x2) / 2
        self.cy = (y1 + y2) / 2
        
        self.radius = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) / 2
        self.initial_angle = math.atan2(y2 - y1, x2 - x1)
        
        self._update_geometry()

    def update(self, dt: float) -> None:
        if self.rotation_speed != 0:
            self.angle += self.rotation_speed * dt
            self._update_geometry()

    def _update_geometry(self) -> None:
        self.x1 = self.cx - math.cos(self.initial_angle + self.angle) * self.radius
        self.y1 = self.cy - math.sin(self.initial_angle + self.angle) * self.radius
        self.x2 = self.cx + math.cos(self.initial_angle + self.angle) * self.radius
        self.y2 = self.cy + math.sin(self.initial_angle + self.angle) * self.radius
        
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        self.length = math.sqrt(dx * dx + dy * dy)
        if self.length > 0:
            self.dir_x = dx / self.length
            self.dir_y = dy / self.length
            self.normal_x = -self.dir_y
            self.normal_y = self.dir_x
        else:
            self.dir_x, self.dir_y = 1.0, 0.0
            self.normal_x, self.normal_y = 0.0, 1.0

    def get_closest_point(self, px: float, py: float) -> tuple[float, float]:
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        if self.length == 0: return self.x1, self.y1
        t = ((px - self.x1) * dx + (py - self.y1) * dy) / (self.length * self.length)
        t = max(0.0, min(1.0, t))
        return self.x1 + t * dx, self.y1 + t * dy

    def get_corners(self) -> list[tuple[float, float]]:
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def contains(self, px: float, py: float) -> bool:
        return False