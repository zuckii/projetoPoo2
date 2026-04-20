import pygame
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.circle import Circle
from aeroSim.entities.wedge import Wedge
from aeroSim.entities.roof import Roof

class Renderer:
    def __init__(self, width, height, gridRes):
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("Aero Simulator")
        self.gridRes = gridRes
        self.font = pygame.font.Font(None, 36)

    def render(self, world):
        self.screen.fill((30, 30, 30))
        
        # Desenhar obstáculos
        for obs in world.obstacles.getAll():
            if isinstance(obs, Circle):
                # Desenhar círculo
                pygame.draw.circle(self.screen, (150, 150, 150), (int(obs.cx), int(obs.cy)), int(obs.radius), 2)
                pygame.draw.circle(self.screen, (100, 100, 100), (int(obs.cx), int(obs.cy)), int(obs.radius) - 2)
            elif isinstance(obs, Polygon):
                # Desenhar polígono (retângulo)
                corners = obs.getCorners()
                points = [(int(x), int(y)) for x, y in corners]
                pygame.draw.polygon(self.screen, (100, 100, 150), points)
                pygame.draw.polygon(self.screen, (150, 150, 200), points, 2)
            elif isinstance(obs, Wedge):
                # Desenhar funil em V
                corners = obs.getCorners()
                points = [(int(x), int(y)) for x, y in corners]
                pygame.draw.polygon(self.screen, (120, 100, 150), points)
                pygame.draw.polygon(self.screen, (180, 150, 220), points, 3)
            elif isinstance(obs, Roof):
                # Desenhar telhado (linha inclinada)
                corners = obs.getCorners()
                if len(corners) == 2:
                    p1 = (int(corners[0][0]), int(corners[0][1]))
                    p2 = (int(corners[1][0]), int(corners[1][1]))
                    pygame.draw.line(self.screen, (200, 200, 200), p1, p2, 4)
        
        # SANDBOX: Desenhar múltiplas partículas
        if hasattr(world, 'particles') and world.particles:
            for particle in world.getAliveParticles():
                # Cor baseado em velocidade (efeito visual)
                speed = (particle.vx**2 + particle.vy**2)**0.5
                color_intensity = min(255, int(50 + speed / 2))
                color = (255, min(255, color_intensity // 2), 50)
                
                pygame.draw.circle(
                    self.screen, 
                    color, 
                    (int(particle.x), int(particle.y)), 
                    int(particle.radius)
                )
        
        # FLUID: Desenhar partícula única (compatibilidade)
        if hasattr(world, 'particle') and world.particle:
            pygame.draw.circle(
                self.screen, 
                (255, 50, 50), 
                (int(world.particle.x), int(world.particle.y)), 
                8
            )
        
        # Desenhar informações
        mode_text = f"Mode: {world.mode} | Particles: {len(world.particles) if hasattr(world, 'particles') else 0}"
        text_surface = self.font.render(mode_text, True, (200, 200, 200))
        self.screen.blit(text_surface, (20, 20))
        
        pygame.display.flip()