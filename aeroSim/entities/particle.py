class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0.0,
        vy: float = 0.0,
        mass: float = 1.0,
        radius: float = 5.0,
    ) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.is_alive = True

    def update_position(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def apply_acceleration(self, ax: float, ay: float, dt: float) -> None:
        self.vx += ax * dt
        self.vy += ay * dt

    def bounce(self, normal_x: float, normal_y: float, damping: float = 0.2) -> None:
        dot = self.vx * normal_x + self.vy * normal_y
        if dot > 0:
            return

        vn_x = dot * normal_x
        vn_y = dot * normal_y
        vt_x = self.vx - vn_x
        vt_y = self.vy - vn_y

        friction = 0.01
        self.vx = (-vn_x * damping) + (vt_x * (1.0 - friction))
        self.vy = (-vn_y * damping) + (vt_y * (1.0 - friction))