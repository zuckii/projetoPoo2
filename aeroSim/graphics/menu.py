import pygame
import sys
import ctypes
from aeroSim.persistence.repository import PersistenceRepository

class Menu:
    def __init__(self):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass

        pygame.init()
        user32 = ctypes.windll.user32
        self.w = user32.GetSystemMetrics(0)
        self.h = user32.GetSystemMetrics(1)

        self.screen = pygame.display.set_mode((850, 600))
        pygame.display.set_caption("AeroSim - Selecionar Mapa")
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        self.repo = PersistenceRepository()
        
        self.btn_default = pygame.Rect(50, 200, 200, 150)
        self.btn_funnel = pygame.Rect(300, 200, 200, 150)
        self.btn_dk2 = pygame.Rect(550, 200, 200, 150)
        
        self.w_scale = 200 / self.w
        self.h_scale = 150 / self.h

    def _draw_preview(self, map_name, rect):
        ramps = self.repo.get_maps(map_name)
        for ramp in ramps:
            p1 = (rect.x + int(ramp.x_start * self.w_scale), rect.y + int(ramp.y_start * self.h_scale))
            p2 = (rect.x + int(ramp.x_end * self.w_scale), rect.y + int(ramp.y_end * self.h_scale))
            pygame.draw.line(self.screen, (255, 100, 200), p1, p2, 2)

    def show(self):
        running = True
        selected_map = None

        while running:
            self.screen.fill((30, 30, 30))
            
            title = self.font.render("Selecione o Mapa", True, (255, 255, 255))
            self.screen.blit(title, (280, 50))
            
            mouse_pos = pygame.mouse.get_pos()
            
            pygame.draw.rect(self.screen, (60, 60, 80), self.btn_default)
            pygame.draw.rect(self.screen, (200, 200, 200), self.btn_default, 2)
            self._draw_preview("default", self.btn_default)
            self.screen.blit(self.small_font.render("Default", True, (255,255,255)), (110, 210))
            
            pygame.draw.rect(self.screen, (60, 60, 80), self.btn_funnel)
            pygame.draw.rect(self.screen, (200, 200, 200), self.btn_funnel, 2)
            self._draw_preview("funnel", self.btn_funnel)
            self.screen.blit(self.small_font.render("Funnel", True, (255,255,255)), (370, 210))

            pygame.draw.rect(self.screen, (60, 60, 80), self.btn_dk2)
            pygame.draw.rect(self.screen, (200, 200, 200), self.btn_dk2, 2)
            self._draw_preview("dk2", self.btn_dk2)
            self.screen.blit(self.small_font.render("DK 2.0", True, (255,255,255)), (620, 210))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_default.collidepoint(mouse_pos):
                        selected_map = "default"
                        running = False
                    elif self.btn_funnel.collidepoint(mouse_pos):
                        selected_map = "funnel"
                        running = False
                    elif self.btn_dk2.collidepoint(mouse_pos):
                        selected_map = "dk2"
                        running = False
                        
            pygame.display.flip()
            
        pygame.quit()
        return selected_map