import math
from aeroSim.config import physicsConfig as physConfig
from aeroSim.entities.circle import Circle
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.wedge import Wedge
from aeroSim.entities.roof import Roof

class AeroSolver:
    def __init__(self, model):
        self.model = model

    def step(self, world, dt):
        """Step para FLUID mode"""
        self.model.solve(world.grid, world.obstacles, dt, particle=world.particle)
    
    def stepSandbox(self, world, dt):
        """Step para SANDBOX mode"""
        particles = world.getAliveParticles()
        
        for particle in particles:
            # 1. Aplicar gravidade
            gravity_force_x = 0
            gravity_force_y = physConfig.GRAVITY
            particle.applyVelocity(gravity_force_x, gravity_force_y, dt)
            
            # 2. Atualizar posição
            particle.updatePosition(dt)
            
            # 3. Verificar colisões com obstáculos
            self._checkObstacleCollisions(particle, world)
            
            # 4. Verificar limites da tela
            self._checkBounds(particle, world)
        
        # 5. Depois de mover tudo, verificar colisões entre partículas
        self._checkParticleCollisions(particles)
    
    def _checkObstacleCollisions(self, particle, world):
        """Detecta e resolve colisões entre partícula e obstáculos"""
        for obs in world.obstacles.getAll():
            if isinstance(obs, Circle):
                self._checkCircleCollision(particle, obs)
            elif isinstance(obs, Polygon):
                self._checkPolygonCollision(particle, obs)
            elif isinstance(obs, Wedge):
                self._checkWedgeCollision(particle, obs)
            elif isinstance(obs, Roof):
                self._checkRoofCollision(particle, obs)
    
    def _checkParticleCollisions(self, particles):
        """Detecta e resolve colisões entre partículas (círculo vs círculo)"""
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                p1 = particles[i]
                p2 = particles[j]
                
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist = math.sqrt(dx*dx + dy*dy)
                
                min_dist = p1.radius + p2.radius
                
                # Se há colisão
                if dist < min_dist and dist > 0.01:
                    # Normal de colisão (da p1 pra p2)
                    nx = dx / dist
                    ny = dy / dist
                    
                    # Separar as partículas
                    overlap = min_dist - dist
                    separation = overlap / 2 + 0.5
                    
                    p1.x -= nx * separation
                    p1.y -= ny * separation
                    p2.x += nx * separation
                    p2.y += ny * separation
                    
                    # Velocidades relativas
                    dvx = p2.vx - p1.vx
                    dvy = p2.vy - p1.vy
                    
                    # Componente normal da velocidade relativa
                    dvn = dvx * nx + dvy * ny
                    
                    # Só resolver se estão se aproximando
                    if dvn < 0:
                        # Impulso (semi-elástico com damping)
                        damping = physConfig.BOUNCE_DAMPING
                        impulse = -(1 + damping) * dvn / (1/p1.mass + 1/p2.mass)
                        
                        # Aplicar impulso
                        p1.vx -= impulse * nx / p1.mass
                        p1.vy -= impulse * ny / p1.mass
                        p2.vx += impulse * nx / p2.mass
                        p2.vy += impulse * ny / p2.mass
    
    def _checkCircleCollision(self, particle, obstacle):
        """Detecta colisão entre partícula (círculo) e obstáculo círculo"""
        dx = particle.x - obstacle.cx
        dy = particle.y - obstacle.cy
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < (obstacle.radius + particle.radius):
            # Normal normalizado
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                nx, ny = 1, 0
            
            # Separar partícula do obstáculo
            overlap = (obstacle.radius + particle.radius) - dist
            particle.x += nx * overlap
            particle.y += ny * overlap
            
            # Aplicar bounce
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
    
    def _checkPolygonCollision(self, particle, obs):
        """Detecta colisão entre partícula e polígono (AABB)"""
        # Cálculo de AABB simples
        half_w = obs.width / 2
        half_h = obs.height / 2
        
        left = obs.x - half_w
        right = obs.x + half_w
        top = obs.y - half_h
        bottom = obs.y + half_h
        
        # Encontrar ponto mais próximo no retângulo
        closest_x = max(left, min(particle.x, right))
        closest_y = max(top, min(particle.y, bottom))
        
        # Calcular distância até o ponto mais próximo
        dx = particle.x - closest_x
        dy = particle.y - closest_y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Se está colidindo
        if dist < particle.radius:
            # Determinar normal de colisão
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                # Se está dentro do retângulo, sair pela face mais próxima
                if abs(dx) > abs(dy):
                    nx = 1 if dx > 0 else -1
                    ny = 0
                else:
                    nx = 0
                    ny = 1 if dy > 0 else -1
            
            # Separar partícula do obstáculo
            overlap = particle.radius - dist
            particle.x += nx * (overlap + 1)
            particle.y += ny * (overlap + 1)
            
            # Aplicar bounce
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
    
    def _checkWedgeCollision(self, particle, obs):
        """Detecta colisão entre partícula e calha V (wedge)"""
        # Verificar se a partícula atravessou a parede
        if not obs.contains(particle.x, particle.y):
            # Encontrar ponto mais próximo na parede
            closest_x, closest_y = obs.getClosestPointOnWall(particle.x, particle.y)
            
            dx = particle.x - closest_x
            dy = particle.y - closest_y
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Se está colidindo com a parede
            if dist < particle.radius:
                # Normal de colisão
                if dist > 0.01:
                    nx = dx / dist
                    ny = dy / dist
                else:
                    nx, ny = obs.getCollisionNormal(particle.x, particle.y)
                
                # Separar partícula da parede
                penetration = particle.radius - dist
                particle.x += nx * (penetration + 1)
                particle.y += ny * (penetration + 1)
                
                # Refletir velocidade
                particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
        else:
            # Partícula DENTRO da calha (erro/penetração)
            # Empurrar para fora
            nx, ny = obs.getCollisionNormal(particle.x, particle.y)
            particle.x -= nx * (particle.radius + 2)
            particle.y -= ny * (particle.radius + 2)
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)

    def _checkRoofCollision(self, particle, roof):
        """Detecta e resolve colisões blindadas para linhas finas"""
        cx, cy = roof.getClosestPoint(particle.x, particle.y)
        
        dx = particle.x - cx
        dy = particle.y - cy
        dist_sq = dx*dx + dy*dy
        
        if dist_sq < particle.radius**2:
            dist = math.sqrt(dist_sq) if dist_sq > 0 else 0.1
            
            # Puxa a normal oficial do telhado
            nx, ny = roof.normal_x, roof.normal_y
            
            # Garante que a normal sempre aponta contra a gravidade (y negativo)
            if ny > 0:
                nx, ny = -nx, -ny
                
            # Verifica se a bola "atravessou" a linha no frame anterior
            dot_pos = dx * nx + dy * ny
            if dot_pos < 0:
                dist = -dist # A bola está do lado de baixo, precisamos empurrar mais!
                
            # Desloca a partícula para cima da linha
            overlap = particle.radius - dist
            if overlap > 0:
                particle.x += nx * overlap
                particle.y += ny * overlap
                
                # Usa o novo bounce escorregadio
                particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING)
    
    def _checkBounds(self, particle, world):
        """Remove partículas que saíram dos limites da tela"""
        margin = 100
        if (particle.x < -margin or 
            particle.x > world.screenWidth + margin or
            particle.y > world.screenHeight + margin):
            particle.isAlive = False