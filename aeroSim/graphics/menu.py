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
        pygame.display.set_caption("AeroSim")
        
        self.font_title = pygame.font.Font(None, 54)
        self.font_subtitle = pygame.font.Font(None, 28)
        self.font_normal = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        self.repo = PersistenceRepository(preserve_data=True)
        
        self.btn_default = pygame.Rect(300, 150, 240, 200)
        self.btn_funnel = pygame.Rect(580, 150, 240, 200)
        self.btn_dk2 = pygame.Rect(860, 150, 240, 200)
        
        self.particle_count = 1000
        self.count_options = [1000, 1500, 2000, 2500]
        
        start_x = 700 - (len(self.count_options) * 140) // 2
        self.count_buttons = [pygame.Rect(start_x + i * 140, 350, 120, 50) for i in range(len(self.count_options))]
        
        self.w_scale = 240 / self.w
        self.h_scale = 200 / self.h

        self.bg_color = (25, 27, 31)
        self.panel_color = (35, 38, 44)
        self.hover_color = (50, 55, 63)
        self.text_main = (240, 240, 245)
        self.text_sub = (150, 160, 170)
        self.accent = (85, 170, 255)
        self.success = (100, 200, 130)

    def _draw_preview(self, map_name, rect):
        ramps = self.repo.get_maps(map_name)
        for ramp in ramps:
            p1 = (rect.x + int(ramp.x_start * self.w_scale), rect.y + int(ramp.y_start * self.h_scale))
            p2 = (rect.x + int(ramp.x_end * self.w_scale), rect.y + int(ramp.y_end * self.h_scale))
            pygame.draw.line(self.screen, (50, 130, 255), p1, p2, 2)

    def _draw_test_results_table(self):
        results = self.repo.get_latest_test_results(limit=8)
        y_offset = 420
        
        pygame.draw.rect(self.screen, self.panel_color, (300, y_offset, 800, 280), border_radius=10)
        
        title = self.font_subtitle.render("Histórico de Testes", True, self.text_main)
        self.screen.blit(title, (330, y_offset + 20))
        
        y_offset += 70
        
        headers = ["Mapa", "Partículas", "Tempo (s)", "Fluxo (p/s)", "Status"]
        x_offsets = [330, 480, 630, 780, 930]
        
        for h, x in zip(headers, x_offsets):
            lbl = self.font_small.render(h, True, self.text_sub)
            self.screen.blit(lbl, (x, y_offset))
            
        y_offset += 30
        pygame.draw.line(self.screen, (60, 65, 75), (330, y_offset), (1070, y_offset), 2)
        y_offset += 15
        
        if not results:
            msg = self.font_normal.render("Nenhum teste executado.", True, self.text_sub)
            self.screen.blit(msg, (330, y_offset + 10))
            return
        
        for i, result in enumerate(results):
            status_text = result.status or 'Concluído'
            if status_text == 'Não concluído':
                color = (220, 80, 80)
            elif i == 0:
                color = self.success
            else:
                color = self.text_main
            
            texts = [
                str(result.map_name).title(),
                str(result.particles_count),
                f"{result.total_time:.2f}",
                f"{result.particles_per_second:.1f}",
                status_text
            ]
            
            for t, x in zip(texts, x_offsets):
                lbl = self.font_small.render(t, True, color)
                self.screen.blit(lbl, (x, y_offset))
                
            y_offset += 25

    def get_particle_count(self):
        selecting = True
        while selecting:
            self.screen.fill(self.bg_color)
            
            title = self.font_title.render("Configuração de Teste", True, self.text_main)
            self.screen.blit(title, (title.get_rect(center=(700, 200))))

            info = self.font_subtitle.render("Selecione a quantidade de partículas:", True, self.text_sub)
            self.screen.blit(info, (info.get_rect(center=(700, 260))))

            for i, count in enumerate(self.count_options):
                btn = self.count_buttons[i]
                is_hover = btn.collidepoint(pygame.mouse.get_pos())
                color = self.hover_color if is_hover else self.panel_color
                
                pygame.draw.rect(self.screen, color, btn, border_radius=8)
                if is_hover:
                    pygame.draw.rect(self.screen, self.accent, btn, 2, border_radius=8)
                    
                label = self.font_normal.render(str(count), True, self.text_main)
                self.screen.blit(label, label.get_rect(center=btn.center))

            instr = self.font_small.render("Pressione ESC para sair", True, (100, 110, 120))
            self.screen.blit(instr, (instr.get_rect(center=(700, 450))))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, btn in enumerate(self.count_buttons):
                        if btn.collidepoint(event.pos):
                            self.particle_count = self.count_options[i]
                            selecting = False
                            break

            pygame.display.flip()

        return self.particle_count

    def show(self):
        running = True
        selected_map = None
        
        change_btn = pygame.Rect(1150, 40, 180, 40)

        while running:
            self.screen.fill(self.bg_color)
            mouse_pos = pygame.mouse.get_pos()
            
            title = self.font_title.render("AeroSim", True, self.text_main)
            self.screen.blit(title, (300, 40))
            
            subtitle = self.font_subtitle.render("Selecione o ambiente de simulação", True, self.text_sub)
            self.screen.blit(subtitle, (300, 90))
            
            btn_color = self.hover_color if change_btn.collidepoint(mouse_pos) else self.panel_color
            pygame.draw.rect(self.screen, btn_color, change_btn, border_radius=8)
            lbl_part = self.font_small.render(f"Partículas: {self.particle_count} (Alterar)", True, self.accent)
            self.screen.blit(lbl_part, lbl_part.get_rect(center=change_btn.center))

            buttons = [
                (self.btn_default, "Default"),
                (self.btn_funnel, "Funnel"),
                (self.btn_dk2, "DK 2.0")
            ]

            for rect, name in buttons:
                is_hover = rect.collidepoint(mouse_pos)
                color = self.hover_color if is_hover else self.panel_color
                
                pygame.draw.rect(self.screen, color, rect, border_radius=12)
                if is_hover:
                    pygame.draw.rect(self.screen, self.accent, rect, 2, border_radius=12)
                    
                self._draw_preview(name.lower().replace(" ", "").replace(".0", ""), rect)
                
                lbl = self.font_normal.render(name, True, self.text_main)
                self.screen.blit(lbl, (rect.x + 20, rect.y + 160))
            
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