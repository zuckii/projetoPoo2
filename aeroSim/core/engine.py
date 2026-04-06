import pygame
import sys

class Engine:
    def __init__(self, fpsLimit):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fpsLimit = fpsLimit
        self.isRunning = True

        infoObject = pygame.display.Info()
        self.screenWidth = infoObject.current_w
        self.screenHeight = infoObject.current_h

    def updateTime(self):
        dt = self.clock.tick(self.fpsLimit) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.isRunning = False
                pygame.quit()
                sys.exit()
        return dt