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

        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("AeroSim - Menu Principal")
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)
        
        self.repo = PersistenceRepository()
        
        # Botões de mapas
        self.btn_default = pygame.Rect(50, 120, 180, 150)
        self.btn_funnel = pygame.Rect(310, 120, 180, 150)
        self.btn_dk2 = pygame.Rect(570, 120, 180, 150)
        
        # Botão de teste
        self.btn_test = pygame.Rect(830, 120, 150, 150)
        
        self.w_scale = 180 / self.w
        self.h_scale = 150 / self.h

    def _draw_preview(self, map_name, rect):
        ramps = self.repo.get_maps(map_name)
        for ramp in ramps:
            p1 = (rect.x + int(ramp.x_start * self.w_scale), rect.y + int(ramp.y_start * self.h_scale))
            p2 = (rect.x + int(ramp.x_end * self.w_scale), rect.y + int(ramp.y_end * self.h_scale))
            pygame.draw.line(self.screen, (255, 100, 200), p1, p2, 2)

    def _draw_test_results(self):
        """Desenha os últimos resultados de testes"""
        results = self.repo.get_latest_test_results(limit=5)
        
        y_offset = 320
        
        # Título
        title = self.small_font.render("Últimos Testes:", True, (100, 255, 100))
        self.screen.blit(title, (50, y_offset))
        
        y_offset += 40
        
        if not results:
            no_tests = self.tiny_font.render("Nenhum teste executado ainda", True, (150, 150, 150))
            self.screen.blit(no_tests, (50, y_offset))
            return
        
        for i, result in enumerate(results):
            # Formato: "Mapa | Tempo: X.XXs | Fluxo: Y.YY part/s"
            text = f"{result.map_name.upper()} | Tempo: {result.total_time:.2f}s | Fluxo: {result.particles_per_second:.1f} part/s"
            color = (200, 200, 200)
            
            # Destacar resultado mais recente
            if i == 0:
                color = (100, 255, 100)
            
            result_text = self.tiny_font.render(text, True, color)
            self.screen.blit(result_text, (50, y_offset))
            y_offset += 25

    def show(self):
        running = True
        selected_map = None
        run_test = False

        while running:
            self.screen.fill((30, 30, 30))
            
            # Título
            title = self.font.render("AeroSim - Menu Principal", True, (255, 255, 255))
            self.screen.blit(title, (250, 20))
            
            subtitle = self.small_font.render("Selecione o Mapa ou Execute um Teste", True, (200, 200, 200))
            self.screen.blit(subtitle, (250, 70))
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Botão Default
            btn_color = (100, 100, 120) if self.btn_default.collidepoint(mouse_pos) else (60, 60, 80)
            pygame.draw.rect(self.screen, btn_color, self.btn_default)
            pygame.draw.rect(self.screen, (200, 200, 200), self.btn_default, 2)
            self._draw_preview("default", self.btn_default)
            self.screen.blit(self.small_font.render("Default", True, (255,255,255)), (80, 135))
            
            # Botão Funnel
            btn_color = (100, 100, 120) if self.btn_funnel.collidepoint(mouse_pos) else (60, 60, 80)
            pygame.draw.rect(self.screen, btn_color, self.btn_funnel)
            pygame.draw.rect(self.screen, (200, 200, 200), self.btn_funnel, 2)
            self._draw_preview("funnel", self.btn_funnel)
            self.screen.blit(self.small_font.render("Funnel", True, (255,255,255)), (355, 135))

            # Botão DK2
            btn_color = (100, 100, 120) if self.btn_dk2.collidepoint(mouse_pos) else (60, 60, 80)
            pygame.draw.rect(self.screen, btn_color, self.btn_dk2)
            pygame.draw.rect(self.screen, (200, 200, 200), self.btn_dk2, 2)
            self._draw_preview("dk2", self.btn_dk2)
            self.screen.blit(self.small_font.render("DK 2.0", True, (255,255,255)), (605, 135))
            
            # Botão Teste
            btn_color = (150, 100, 100) if self.btn_test.collidepoint(mouse_pos) else (80, 60, 60)
            pygame.draw.rect(self.screen, btn_color, self.btn_test)
            pygame.draw.rect(self.screen, (200, 100, 100), self.btn_test, 2)
            self.screen.blit(self.small_font.render("Teste", True, (255,200,200)), (865, 150))
            self.screen.blit(self.tiny_font.render("1000 part", True, (200,150,150)), (850, 190))
            
            # Desenhar resultados dos testes
            self._draw_test_results()
            
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
                    elif self.btn_test.collidepoint(mouse_pos):
                        run_test = True
                        running = False
                        
            pygame.display.flip()
            
        pygame.quit()
        
        if run_test:
            return "test"  # Retorna string indicando modo teste
        else:
            return selected_map if selected_map else None