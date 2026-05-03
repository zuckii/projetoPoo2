import math
from aeroSim.config import physicsConfig as physConfig
from aeroSim.entities.circle import Circle
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.wedge import Wedge
from aeroSim.entities.roof import Roof
from aeroSim.entities.simplePlatform import SimplePlatform

class AeroSolver:
    def __init__(self, model):
        self.model = model

    def step(self, world, dt):
        """Step para FLUID mode"""
        self.model.solve(world.grid, world.obstacles, dt, particle=world.particle)
    
    def stepSandbox(self, world, dt):
        """Step para SANDBOX mode usando Sub-stepping para evitar clipping"""
        particles = world.getAliveParticles()
        if not particles:
            return
            
        # Divide o cálculo da física em passos menores para maior precisão
        sub_steps = 4 
        sub_dt = dt / sub_steps
        
        for _ in range(sub_steps):
            # 1. Aplicar gravidade, atualizar posição e checar limites
            for particle in particles:
                gravity_force_x = 0
                gravity_force_y = physConfig.GRAVITY
                
                particle.applyVelocity(gravity_force_x, gravity_force_y, sub_dt)
                particle.updatePosition(sub_dt)
                self._checkBounds(particle, world)
            
            # 2. PRIMEIRO: Resolver colisões entre partículas
            self._checkParticleCollisions(particles)
            
            # 3. POR ÚLTIMO: Resolver colisões com obstáculos
            for particle in particles:
                self._checkObstacleCollisions(particle, world)
                
    def _checkObstacleCollisions(self, particle, world):
        """Detecta e resolve colisões entre partícula e obstáculos"""
        for obs in world.obstacles.getAll():
            if isinstance(obs, Circle):
                self._checkCircleCollision(particle, obs)
            elif isinstance(obs, SimplePlatform):
                self._checkRoofCollision(particle, obs)
            elif isinstance(obs, Polygon):
                self._checkPolygonCollision(particle, obs)
            elif isinstance(obs, Wedge):
                self._checkWedgeCollision(particle, obs)
            elif isinstance(obs, Roof):
                self._checkRoofCollision(particle, obs)
    
    def _checkParticleCollisions(self, particles):
        """Detecta e resolve colisões usando um Spatial Grid para evitar O(N^2)"""
        if not particles: return

        cell_size = 15.0 
        grid = {}

        for p in particles:
            cell_x = int(p.x // cell_size)
            cell_y = int(p.y // cell_size)
            cell = (cell_x, cell_y)
            
            if cell not in grid:
                grid[cell] = []
            grid[cell].append(p)

        checked_pairs = set()

        for cell, cell_particles in grid.items():
            cx, cy = cell
            
            neighbors = [
                (cx-1, cy-1), (cx, cy-1), (cx+1, cy-1),
                (cx-1, cy),   (cx, cy),   (cx+1, cy),
                (cx-1, cy+1), (cx, cy+1), (cx+1, cy+1)
            ]

            for neighbor in neighbors:
                if neighbor not in grid:
                    continue
                    
                neighbor_particles = grid[neighbor]
                
                for p1 in cell_particles:
                    for p2 in neighbor_particles:
                        if p1 is p2:
                            continue
                        
                        pair_id = tuple(sorted((id(p1), id(p2))))
                        if pair_id in checked_pairs:
                            continue
                        checked_pairs.add(pair_id)

                        dx = p2.x - p1.x
                        dy = p2.y - p1.y
                        dist_sq = dx*dx + dy*dy
                        
                        min_dist = p1.radius + p2.radius
                        
                        if dist_sq < (min_dist * min_dist) and dist_sq > 0.0001:
                            dist = math.sqrt(dist_sq)
                            nx = dx / dist
                            ny = dy / dist
                            
                            overlap = min_dist - dist
                            separation = overlap / 2 + 0.5
                            
                            p1.x -= nx * separation
                            p1.y -= ny * separation
                            p2.x += nx * separation
                            p2.y += ny * separation
                            
                            dvx = p2.vx - p1.vx
                            dvy = p2.vy - p1.vy
                            dvn = dvx * nx + dvy * ny
                            
                            if dvn < 0:
                                damping = physConfig.BOUNCE_DAMPING
                                impulse = -(1 + damping) * dvn / (1/p1.mass + 1/p2.mass)
                                
                                p1.vx -= impulse * nx / p1.mass
                                p1.vy -= impulse * ny / p1.mass
                                p2.vx += impulse * nx / p2.mass
                                p2.vy += impulse * ny / p2.mass
    
    def _checkCircleCollision(self, particle, obstacle):
        dx = particle.x - obstacle.cx
        dy = particle.y - obstacle.cy
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < (obstacle.radius + particle.radius):
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                nx, ny = 1, 0
            
            overlap = (obstacle.radius + particle.radius) - dist
            particle.x += nx * overlap
            particle.y += ny * overlap
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
    
    def _checkPolygonCollision(self, particle, obs):
        half_w = obs.width / 2
        half_h = obs.height / 2
        
        left = obs.x - half_w
        right = obs.x + half_w
        top = obs.y - half_h
        bottom = obs.y + half_h
        
        closest_x = max(left, min(particle.x, right))
        closest_y = max(top, min(particle.y, bottom))
        
        dx = particle.x - closest_x
        dy = particle.y - closest_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < particle.radius:
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                if abs(dx) > abs(dy):
                    nx = 1 if dx > 0 else -1
                    ny = 0
                else:
                    nx = 0
                    ny = 1 if dy > 0 else -1
            
            overlap = particle.radius - dist
            particle.x += nx * (overlap + 1)
            particle.y += ny * (overlap + 1)
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
    
    def _checkWedgeCollision(self, particle, obs):
        if not obs.contains(particle.x, particle.y):
            closest_x, closest_y = obs.getClosestPointOnWall(particle.x, particle.y)
            dx = particle.x - closest_x
            dy = particle.y - closest_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < particle.radius:
                if dist > 0.01:
                    nx = dx / dist
                    ny = dy / dist
                else:
                    nx, ny = obs.getCollisionNormal(particle.x, particle.y)
                
                penetration = particle.radius - dist
                particle.x += nx * (penetration + 1)
                particle.y += ny * (penetration + 1)
                particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
        else:
            nx, ny = obs.getCollisionNormal(particle.x, particle.y)
            particle.x -= nx * (particle.radius + 2)
            particle.y -= ny * (particle.radius + 2)
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)

    def _checkRoofCollision(self, particle, roof):
        cx, cy = roof.getClosestPoint(particle.x, particle.y)
        dx = particle.x - cx
        dy = particle.y - cy
        dist_sq = dx*dx + dy*dy
        
        if dist_sq < particle.radius**2:
            dist = math.sqrt(dist_sq) if dist_sq > 0 else 0.1
            nx, ny = roof.normal_x, roof.normal_y
            
            if ny > 0:
                nx, ny = -nx, -ny
                
            dot_pos = dx * nx + dy * ny
            if dot_pos < 0:
                dist = -dist 
                
            overlap = particle.radius - dist
            if overlap > 0:
                particle.x += nx * overlap
                particle.y += ny * overlap
                particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
    
    def _checkBounds(self, particle, world):
        margin = 100
        if (particle.x < -margin or 
            particle.x > world.screenWidth + margin or
            particle.y > world.screenHeight + margin):
            particle.isAlive = False