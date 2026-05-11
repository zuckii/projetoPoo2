import pygame
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.circle import Circle
from aeroSim.entities.roof import Roof


class Renderer:
    def __init__(self, width: int, height: int) -> None:
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("Aero Simulator")
        self.font = pygame.font.Font(None, 36)
        self.offset_y = 0

    def render(self, world) -> None:
        self.screen.fill((30, 30, 30))

        for obs in world.obstacles:
            if isinstance(obs, Circle):
                pygame.draw.circle(
                    self.screen,
                    (150, 150, 150),
                    (int(obs.cx), int(obs.cy + self.offset_y)),
                    int(obs.radius),
                    2,
                )
                pygame.draw.circle(
                    self.screen,
                    (100, 100, 100),
                    (int(obs.cx), int(obs.cy + self.offset_y)),
                    int(obs.radius) - 2,
                )
            elif isinstance(obs, Polygon):
                corners = obs.get_corners()
                points = [(int(x), int(y + self.offset_y)) for x, y in corners]
                pygame.draw.polygon(self.screen, (100, 100, 150), points)
                pygame.draw.polygon(self.screen, (150, 150, 200), points, 2)
            elif isinstance(obs, Roof):
                corners = obs.get_corners()
                if len(corners) == 2:
                    p1 = (int(corners[0][0]), int(corners[0][1] + self.offset_y))
                    p2 = (int(corners[1][0]), int(corners[1][1] + self.offset_y))
                    pygame.draw.line(self.screen, (220, 20, 150), p1, p2, 8)
                    pygame.draw.line(self.screen, (255, 100, 200), p1, p2, 4)

        for particle in world.get_alive_particles():
            speed = (particle.vx**2 + particle.vy**2) ** 0.5
            color_intensity = min(255, int(50 + speed / 2))
            color = (255, min(255, color_intensity // 2), 50)

            pygame.draw.circle(
                self.screen,
                color,
                (int(particle.x), int(particle.y + self.offset_y)),
                int(particle.radius),
            )

        mode_text = f"Mode: {world.mode} | Particles: {len(world.particles)}"
        text_surface = self.font.render(mode_text, True, (200, 200, 200))
        self.screen.blit(text_surface, (20, 20))

        pygame.display.flip()