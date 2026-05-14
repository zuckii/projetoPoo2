import random
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.roof import Roof
from aeroSim.entities.particle import Particle
from aeroSim.persistence.repository import PersistenceRepository

class World:
    def __init__(self, screen_width: int, screen_height: int, map_name: str = "default") -> None:
        self.obstacles = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_name = map_name

        self.particles = []
        self.spawn_timer = 0.0
        self.spawn_active = False
        
        self.repo = PersistenceRepository()

        self._init_sandbox()
    
    def _init_sandbox(self) -> None:
        screen_w = self.screen_width
        screen_h = self.screen_height
        wall_thickness = max(20, int(screen_w * 0.02))

        self.obstacles.append(Polygon(x=wall_thickness / 2, y=screen_h / 2, width=wall_thickness, height=screen_h))
        self.obstacles.append(Polygon(x=screen_w - wall_thickness / 2, y=screen_h / 2, width=wall_thickness, height=screen_h))

        ramps = self.repo.get_maps(self.map_name)
        for i, ramp in enumerate(ramps):
            speed = 0.0
            if self.map_name == "dk2" and i == 2:
                speed = 1.0
            
            self.obstacles.append(Roof(ramp.x_start, ramp.y_start, ramp.x_end, ramp.y_end, rotation_speed=speed))

        preset = self.repo.get_preset("default")
        self.spawn_interval = preset.spawn_interval if preset else 0.15
        self.spawn_active = True
        self.particles = []

    def spawn_particle(self) -> None:
        wall_thickness = max(20, int(self.screen_width * 0.02))
        x = wall_thickness + 30 + random.uniform(-10, 10)
        y = self.screen_height * 0.02

        vx = random.uniform(1, 4)
        vy = 0.0
        
        radius = random.uniform(3.0, 8.0)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(150, 255))

        self.particles.append(Particle(x=x, y=y, vx=vx, vy=vy, mass=1.0, radius=radius, color=color))

    

    def update(self, dt: float) -> None:
        kill_y_threshold = self.screen_height - 20
        for particle in self.particles:
            if particle.y > kill_y_threshold:
                particle.is_alive = False

        self.particles = [p for p in self.particles if p.is_alive]

        for obs in self.obstacles:
            if hasattr(obs, 'update'):
                obs.update(dt)

        if self.spawn_active:
            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_interval:
                self.spawn_particle()
                self.spawn_timer -= self.spawn_interval

    def get_alive_particles(self) -> list[Particle]:
        return [particle for particle in self.particles if particle.is_alive]