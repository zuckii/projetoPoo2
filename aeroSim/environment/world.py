import random
from aeroSim.environment.fluidGrid import FluidGrid
from aeroSim.entities.circle import Circle
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.roof import Roof
from aeroSim.entities.particle import Particle


class World:
    def __init__(self, grid_res: int, screen_width: int, screen_height: int, mode: str = "SANDBOX") -> None:
        self.grid = FluidGrid(grid_res)
        self.obstacles = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mode = mode

        self.particles = []
        self.spawn_timer = 0.0
        self.spawn_interval = 0.03
        self.spawn_active = False

        if mode == "SANDBOX":
            self._init_sandbox()
        else:
            self._init_fluid()
    
    def _init_sandbox(self) -> None:
        screen_w = self.screen_width
        screen_h = self.screen_height

        wall_thickness = max(20, int(screen_w * 0.02))
        ball_gap = int(screen_w * 0.25)

        n_platforms = 3
        top_margin = screen_h * 0.05
        bottom_margin = screen_h * 0.05
        available_height = screen_h - top_margin - bottom_margin
        vertical_gap = available_height / n_platforms

        ramp_drop = vertical_gap * 0.90

        self.obstacles.append(Polygon(x=wall_thickness / 2, y=screen_h / 2, width=wall_thickness, height=screen_h))
        self.obstacles.append(Polygon(x=screen_w - wall_thickness / 2, y=screen_h / 2, width=wall_thickness, height=screen_h))

        for i in range(n_platforms):
            y_start = top_margin + (i * vertical_gap)
            y_end = y_start + ramp_drop

            if i % 2 == 0:
                x_start = wall_thickness
                x_end = screen_w - ball_gap
            else:
                x_start = screen_w - wall_thickness
                x_end = ball_gap

            self.obstacles.append(Roof(x_start, y_start, x_end, y_end))

        self.spawn_active = True
        self.spawn_interval = 0.09
        self.particles = []

    def spawn_particle(self) -> None:
        wall_thickness = max(20, int(self.screen_width * 0.02))
        x = wall_thickness + 30 + random.uniform(-10, 10)
        y = self.screen_height * 0.02

        vx = random.uniform(1, 4)
        vy = 0.0

        self.particles.append(Particle(x=x, y=y, vx=vx, vy=vy, mass=1.0))

    def _init_fluid(self) -> None:
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        self.obstacles.append(Circle(x=center_x, y=center_y, radius=100))
        self.particles.append(Particle(x=50, y=center_y, vx=300.0, vy=0.0, mass=1.0, radius=8.0))

    def update(self, dt: float) -> None:
        kill_y_threshold = self.screen_height - 20
        for particle in self.particles:
            if particle.y > kill_y_threshold:
                particle.is_alive = False

        self.particles = [particle for particle in self.particles if particle.is_alive]

        if self.spawn_active:
            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_interval:
                self.spawn_particle()
                self.spawn_timer -= self.spawn_interval

    def get_alive_particles(self) -> list[Particle]:
        return [particle for particle in self.particles if particle.is_alive]