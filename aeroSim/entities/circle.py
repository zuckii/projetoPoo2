from aeroSim.entities.obstacle import Obstacle
import math

class Circle(Obstacle):
    def __init__(self, x, y, radius):
        self.cx = x
        self.cy = y
        self.radius = radius

    def contains(self, x, y) -> bool:
        distance = math.sqrt((x - self.cx)**2 + (y - self.cy)**2)
        return distance <= self.radius