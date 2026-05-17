import pygame
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.roof import Roof

class Renderer:
    RAMP_COLOR = (50, 130, 255)

    def __init__(self, width: int, height: int) -> None:
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("Aero Simulator")
        self.font = pygame.font.Font(None, 36)
        self.offset_y = 0

    def render(self, world, show_timer: bool = False, elapsed_time: float = 0.0) -> None:
        self.screen.fill((30, 30, 30))

        for obs in world.obstacles:
            if isinstance(obs, Polygon):
                corners = obs.get_corners()
                points = [(int(x), int(y + self.offset_y)) for x, y in corners]
                pygame.draw.polygon(self.screen, (100, 100, 150), points)
                pygame.draw.polygon(self.screen, (150, 150, 200), points, 2)
            elif isinstance(obs, Roof):
                corners = obs.get_corners()
                if len(corners) == 2:
                    p1 = (int(corners[0][0]), int(corners[0][1] + self.offset_y))
                    p2 = (int(corners[1][0]), int(corners[1][1] + self.offset_y))
                    pygame.draw.line(self.screen, self.RAMP_COLOR, p1, p2, 8)
                    pygame.draw.line(self.screen, self.RAMP_COLOR, p1, p2, 4)

        for particle in world.get_alive_particles():
            pygame.draw.circle(
                self.screen,
                particle.color,
                (int(particle.x), int(particle.y + self.offset_y)),
                int(particle.radius),
            )

        particle_count = len(world.particles)
        text_surface = self.font.render(f"Particles: {particle_count}", True, (200, 200, 200))
        self.screen.blit(text_surface, (20, 20))
        
        # Mostra cronômetro se em modo teste
        if show_timer:
            minutes = int(elapsed_time) // 60
            seconds = int(elapsed_time) % 60
            centiseconds = int((elapsed_time % 1) * 100)
            timer_text = f"{minutes:02d}:{seconds:02d}.{centiseconds:02d}"
            timer_surface = self.font.render(timer_text, True, (0, 255, 100))
            # Posiciona no canto superior direito
            text_width = timer_surface.get_width()
            self.screen.blit(timer_surface, (self.screen.get_width() - text_width - 20, 20))

        pygame.display.flip()