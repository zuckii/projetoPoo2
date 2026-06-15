class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0.0,
        vy: float = 0.0,
        mass: float = 1.0,
        radius: float = 5.0,
        color: tuple = (255, 255, 255),
        friction: float = 0.01
    ) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.friction = friction
        self.is_alive = True

    def update_position(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def apply_acceleration(self, ax: float, ay: float, dt: float) -> None:
        self.vx += ax * dt
        self.vy += ay * dt

    def bounce(self, normal_x: float, normal_y: float, damping: float = 0.2) -> None:
        dot = self.vx * normal_x + self.vy * normal_y
        if dot >= 0:
            return

        vn_x = dot * normal_x
        vn_y = dot * normal_y
        vt_x = self.vx - vn_x
        vt_y = self.vy - vn_y

        new_vn_x = -vn_x * damping
        new_vn_y = -vn_y * damping

        friction_scale = max(0.0, 1.0 - self.friction)
        new_vt_x = vt_x * friction_scale
        new_vt_y = vt_y * friction_scale

        if new_vt_x * new_vt_x + new_vt_y * new_vt_y < 0.01 * 0.01:
            new_vt_x = 0.0
            new_vt_y = 0.0

        self.vx = new_vn_x + new_vt_x
        self.vy = new_vn_y + new_vt_y