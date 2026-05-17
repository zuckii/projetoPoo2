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

        self.screen = pygame.display.set_mode((1400, 750))
        pygame.display.set_caption("AeroSim - Menu Principal")
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)
        self.input_font = pygame.font.Font(None, 36)
        
        self.repo = PersistenceRepository(preserve_data=True)
        
        # Botões de mapas
        self.btn_default = pygame.Rect(50, 120, 180, 150)
        self.btn_funnel = pygame.Rect(310, 120, 180, 150)
        self.btn_dk2 = pygame.Rect(570, 120, 180, 150)
        
        # Input de partículas
        self.input_rect = pygame.Rect(950, 200, 200, 50)
        self.particle_count = 1000
        self.input_active = False
        self.input_text = "1000"
        
        self.w_scale = 180 / self.w
        self.h_scale = 150 / self.h

    def _draw_preview(self, map_name, rect):
        ramps = self.repo.get_maps(map_name)
        for ramp in ramps:
            p1 = (rect.x + int(ramp.x_start * self.w_scale), rect.y + int(ramp.y_start * self.h_scale))
            p2 = (rect.x + int(ramp.x_end * self.w_scale), rect.y + int(ramp.y_end * self.h_scale))
            pygame.draw.line(self.screen, (255, 100, 200), p1, p2, 2)

    def _draw_test_results_table(self):
        """Desenha tabela com últimos 10 resultados de testes"""
        results = self.repo.get_latest_test_results(limit=10)
        
        y_offset = 330
        
        # Título
        title = self.small_font.render("Histórico de Testes", True, (100, 255, 100))
        self.screen.blit(title, (50, y_offset))
        
        y_offset += 40
        
        # Cabeçalho da tabela
        header_text = "Mapa         | Partículas | Tempo (s) | Fluxo (part/s)"
        header = self.tiny_font.render(header_text, True, (200, 200, 100))
        self.screen.blit(header, (50, y_offset))
        
        y_offset += 25
        pygame.draw.line(self.screen, (150, 150, 100), (50, y_offset), (700, y_offset), 1)
        y_offset += 10
        
        if not results:
            no_tests = self.tiny_font.render("Nenhum teste executado ainda", True, (150, 150, 150))
            self.screen.blit(no_tests, (50, y_offset))
            return
        
        for i, result in enumerate(results):
            # Formatar dados para tabela
            map_name = result.map_name.ljust(12)
            particles = str(result.particles_count).ljust(11)
            time_str = f"{result.total_time:.2f}".ljust(10)
            flux_str = f"{result.particles_per_second:.1f}"
            
            row_text = f"{map_name}| {particles}| {time_str}| {flux_str}"
            
            # Cor: verde para resultado mais recente
            color = (100, 255, 100) if i == 0 else (200, 200, 200)
            
            row = self.tiny_font.render(row_text, True, color)
            self.screen.blit(row, (50, y_offset))
            y_offset += 25

    def get_particle_count(self):
        """Tela para o usuário escolher número de partículas"""
        entering = True
        self.input_active = True
        self.input_text = "1000"
        self.particle_count = 1000
        pygame.key.start_text_input()

        while entering:
            self.screen.fill((30, 30, 30))
            
            # Título
            title = self.font.render("Quantas Partículas?", True, (255, 255, 255))
            self.screen.blit(title, (350, 150))
            
            # Info
            info = self.small_font.render("Mínimo: 1000 | Máximo: 5000", True, (200, 200, 200))
            self.screen.blit(info, (350, 250))
            
            # Input box
            pygame.draw.rect(self.screen, (80, 80, 100), self.input_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), self.input_rect, 3)
            
            # Texto no input
            input_surface = self.input_font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(input_surface, (self.input_rect.x + 10, self.input_rect.y + 5))
            
            # Instruções
            instr = self.small_font.render("Pressione ENTER para confirmar", True, (150, 150, 200))
            self.screen.blit(instr, (300, 400))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Valida entrada
                        try:
                            count = int(self.input_text)
                            if 1000 <= count <= 5000:
                                self.particle_count = count
                                entering = False
                            else:
                                self.input_text = "1000"
                        except ValueError:
                            self.input_text = "1000"
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1] if self.input_text else "1000"
                    elif event.key == pygame.K_ESCAPE:
                        entering = False
                        pygame.key.stop_text_input()
                        return None
                elif event.type == pygame.TEXTINPUT:
                    # Para inputs numéricos
                    if event.text.isdigit():
                        self.input_text += event.text
                        if len(self.input_text) > 4:
                            self.input_text = self.input_text[-4:]
            
            pygame.display.flip()
        
        pygame.key.stop_text_input()
        return self.particle_count

    def show(self):
        """Menu para escolher mapa - todos os mapas executam teste"""
        running = True
        selected_map = None

        while running:
            self.screen.fill((30, 30, 30))
            
            # Título
            title = self.font.render("AeroSim - Selecione o Mapa", True, (255, 255, 255))
            self.screen.blit(title, (300, 20))
            
            subtitle = self.small_font.render("Todos os mapas executarão teste com medição de tempo", True, (200, 200, 200))
            self.screen.blit(subtitle, (200, 70))
            
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
            
            # Seção de informações à direita
            info_x = 830
            info_label = self.small_font.render(f"Partículas: {self.particle_count}", True, (100, 200, 255))
            self.screen.blit(info_label, (info_x, 150))
            
            change_btn = pygame.Rect(info_x, 200, 150, 40)
            btn_color = (80, 120, 100) if change_btn.collidepoint(mouse_pos) else (60, 100, 80)
            pygame.draw.rect(self.screen, btn_color, change_btn)
            pygame.draw.rect(self.screen, (200, 200, 200), change_btn, 2)
            self.screen.blit(self.small_font.render("Alterar", True, (255,255,255)), (info_x + 30, 205))
            
            # Desenhar tabela de resultados
            self._draw_test_results_table()
            
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
                    elif change_btn.collidepoint(mouse_pos):
                        count = self.get_particle_count()
                        if count:
                            self.particle_count = count
                        
            pygame.display.flip()
            
        pygame.quit()
        
        return selected_map
