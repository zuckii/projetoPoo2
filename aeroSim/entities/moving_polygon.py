from aeroSim.entities.polygon import Polygon

class MovingPolygon(Polygon):
    def __init__(self, x, y, width, height, min_x, max_x, speed, start_direction=1):
        super().__init__(x=x, y=y, width=width, height=height)
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed
        self.direction = start_direction

    def update(self, dt):
        self.x += self.speed * self.direction * dt

        if self.x <= self.min_x:
            self.x = self.min_x
            self.direction = 1
        elif self.x >= self.max_x:
            self.x = self.max_x
            self.direction = -1

        if hasattr(self, 'body'):
            if hasattr(self.body, 'position'):
                self.body.position = (self.x, self.y)
            if hasattr(self.body, 'velocity'):
                self.body.velocity = (self.speed * self.direction, 0)


class Broom(MovingPolygon):
    def __init__(self, x1, y1, x2, y2, width, height, min_x, max_x, speed, start_direction=-1):
        self.ramp_x1 = x1
        self.ramp_y1 = y1
        self.ramp_x2 = x2
        self.ramp_y2 = y2
        self.min_x = min(min_x, max_x)
        self.max_x = max(min_x, max_x)
        start_x = self.max_x if start_direction < 0 else self.min_x
        super().__init__(x=start_x, y=y1, width=width, height=height,
                         min_x=self.min_x, max_x=self.max_x,
                         speed=speed, start_direction=start_direction)
        self._align_to_ramp()

    def _align_to_ramp(self):
        if self.ramp_x2 == self.ramp_x1:
            self.y = self.ramp_y1
            return

        t = (self.x - self.ramp_x1) / (self.ramp_x2 - self.ramp_x1)
        self.y = self.ramp_y1 + t * (self.ramp_y2 - self.ramp_y1)

    def update(self, dt):
        super().update(dt)
        self._align_to_ramp()