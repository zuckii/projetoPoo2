import pygame
import sys

class Engine:
    def __init__(self, fps_limit: int) -> None:
        self.clock = pygame.time.Clock()
        self.fps_limit = fps_limit
        self.is_running = True

    def update_time(self) -> float:
        dt = self.clock.tick(self.fps_limit) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.is_running = False
                pygame.quit()
                sys.exit()
        return dt