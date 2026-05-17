import random
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.roof import Roof
from aeroSim.entities.particle import Particle
from aeroSim.persistence.repository import PersistenceRepository

class World:
    def __init__(self, screen_width: int, screen_height: int, map_name: str = "default",
                 particle_sequence_name: str = None) -> None:
        self.obstacles = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_name = map_name
        self.particle_sequence_name = particle_sequence_name

        self.particles = []
        self.spawn_timer = 0.0
        self.spawn_active = False
        
        self.spawned_count = 0
        self.target_particles = 150
        self.particles_exited = 0
        self.particle_sequence_data = None
        
        self.repo = PersistenceRepository()
        
        # Carrega sequência persistente se fornecida
        # ... dentro do __init__ do World ...

        if particle_sequence_name:
            self.particle_sequence_data = self.repo.get_particle_sequence(particle_sequence_name)
            if self.particle_sequence_data:
                # Carrega todos os dados da sequência
                self.particle_sequence_data.particles = self.repo.get_sequence_particles(particle_sequence_name)
        
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

        if self.map_name == "default_modified":
            gap = screen_w * 0.25
            self.obstacles.append(Roof(gap - 20, screen_h * 0.6 - 20, gap + 60, screen_h * 0.6 + 20, rotation_speed=2.0))
            self.obstacles.append(Roof(screen_w - gap - 60, screen_h * 0.4 - 20, screen_w - gap + 20, screen_h * 0.4 + 20, rotation_speed=-2.0))

        preset = self.repo.get_preset("default")
        self.spawn_interval = preset.spawn_interval if preset else 0.15
        self.spawn_active = True
        self.particles = []

    def spawn_particle(self) -> None:
        if self.spawned_count >= self.target_particles:
            return

        wall_thickness = max(20, int(self.screen_width * 0.02))
        x = wall_thickness + 30 + random.uniform(-10, 10)
        y = self.screen_height * 0.02

        # Se temos uma sequência persistente, usa os dados dela
        if self.particle_sequence_data and self.particle_sequence_data.particles:
            if self.spawned_count < len(self.particle_sequence_data.particles):
                particle_data = self.particle_sequence_data.particles[self.spawned_count]
                radius = particle_data.radius
                color = (particle_data.color_r, particle_data.color_g, particle_data.color_b)
                vx = particle_data.initial_vx
            else:
                # Fallback se houver mais partículas que dados
                radius = random.uniform(3.0, 8.0)
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(150, 255))
                vx = random.uniform(1, 4)
        else:
            # Geração aleatória normal
            radius = random.uniform(3.0, 8.0)
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(150, 255))
            vx = random.uniform(1, 4)
        
        vy = 0.0

        self.particles.append(Particle(x=x, y=y, vx=vx, vy=vy, mass=1.0, radius=radius, color=color))
        self.spawned_count += 1

    def update(self, dt: float) -> None:
        kill_y_threshold = self.screen_height - 20
        for particle in self.particles:
            if particle.y > kill_y_threshold:
                particle.is_alive = False
                self.particles_exited += 1

        self.particles = [p for p in self.particles if p.is_alive]

        for obs in self.obstacles:
            if hasattr(obs, 'update'):
                obs.update(dt)

        if self.spawn_active and self.spawned_count < self.target_particles:
            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_interval:
                self.spawn_particle()
                self.spawn_timer -= self.spawn_interval

    def get_alive_particles(self) -> list[Particle]:
        return [particle for particle in self.particles if particle.is_alive]