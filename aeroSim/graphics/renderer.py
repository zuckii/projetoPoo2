import pygame

class Renderer:
    def __init__(self, width, height, gridRes):
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("Aero Simulator")
        self.gridRes = gridRes

    def render(self, world):
        self.screen.fill((30, 30, 30))
        
        for obs in world.obstacles.getAll():
            pygame.draw.circle(self.screen, (150, 150, 150), (int(obs.cx), int(obs.cy)), obs.radius)
        
        if hasattr(world, 'particle') and world.particle:
            pygame.draw.circle(self.screen, (255, 50, 50), (int(world.particle.x), int(world.particle.y)), 8)
        
        pygame.display.flip()