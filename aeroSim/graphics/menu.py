import pygame
import sys
import ctypes
from aeroSim.persistence.repository import PersistenceRepository
from aeroSim.graphics.batch_menu import BatchMenu, summarize_batch_results
from aeroSim.graphics.results_screen import ResultsScreen

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

        self.screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("AeroSim - Seleção de Mapas")
        
        self.font_title = pygame.font.Font(None, 54)
        self.font_subtitle = pygame.font.Font(None, 32)
        self.font_normal = pygame.font.Font(None, 26)
        self.font_small = pygame.font.Font(None, 22)
        
        self.repo = PersistenceRepository(preserve_data=True)
        
        self.particle_count = 1000
        self.count_options = [500, 1000, 1500, 2000, 2500]
        
        start_x = 700 - (len(self.count_options) * 140) // 2
        self.count_buttons = [pygame.Rect(start_x + i * 140, 350, 120, 50) for i in range(len(self.count_options))]
        
        self.card_w = 360
        self.card_h = 180
        self.w_scale = self.card_w / self.w
        self.h_scale = self.card_h / self.h

        self.bg_color = (20, 22, 28)
        self.panel_color = (35, 40, 50)
        self.hover_color = (45, 55, 70)
        self.text_main = (250, 250, 255)
        self.text_sub = (170, 180, 190)
        self.accent = (60, 150, 255)
        self.success = (80, 220, 120)

        self.map_names = self.repo.get_map_names()
        self.map_buttons = self._build_map_buttons()
        self.batch_menu = BatchMenu(self)
        self.results_screen = ResultsScreen(self)
        
        self.table_scroll_y = 0
        self.max_table_scroll = 0

    def _draw_mode_selection(self):
        self.screen.fill(self.bg_color)

        title = self.font_title.render("AeroSim", True, self.accent)
        self.screen.blit(title, (title.get_rect(center=(700, 180))))

        subtitle = self.font_subtitle.render("Escolha o modo de execução", True, self.text_sub)
        self.screen.blit(subtitle, (subtitle.get_rect(center=(700, 245))))

        single_btn = pygame.Rect(430, 340, 240, 90)
        batch_btn = pygame.Rect(730, 340, 240, 90)

        mouse_pos = pygame.mouse.get_pos()
        for rect, label in ((single_btn, "Execução única"), (batch_btn, "Batch automático")):
            color = self.hover_color if rect.collidepoint(mouse_pos) else self.panel_color
            pygame.draw.rect(self.screen, color, rect, border_radius=14)
            pygame.draw.rect(self.screen, self.accent, rect, 2, border_radius=14)
            text = self.font_normal.render(label, True, self.text_main)
            self.screen.blit(text, text.get_rect(center=rect.center))

        return single_btn, batch_btn

    def _build_map_buttons(self):
        buttons = []
        columns = 3
        gap_x = 40
        gap_y = 30
        
        total_width = (columns * self.card_w) + ((columns - 1) * gap_x)
        start_x = (1400 - total_width) // 2
        start_y = 160

        for index, map_name in enumerate(self.map_names):
            column = index % columns
            row = index // columns
            x = start_x + column * (self.card_w + gap_x)
            y = start_y + row * (self.card_h + gap_y)
            rect = pygame.Rect(x, y, self.card_w, self.card_h)
            buttons.append((rect, map_name))

        return buttons

    def _draw_preview(self, map_name, rect):
        ramps = self.repo.get_maps(map_name)
        
        preview_bg = pygame.Rect(rect.x + 10, rect.y + 10, rect.width - 20, rect.height - 50)
        pygame.draw.rect(self.screen, (25, 30, 38), preview_bg, border_radius=8)

        for ramp in ramps:
            p1 = (rect.x + 10 + int(ramp.x_start * self.w_scale * 0.9), rect.y + 10 + int(ramp.y_start * self.h_scale * 0.8))
            p2 = (rect.x + 10 + int(ramp.x_end * self.w_scale * 0.9), rect.y + 10 + int(ramp.y_end * self.h_scale * 0.8))
            pygame.draw.line(self.screen, self.accent, p1, p2, 3)

        if map_name == "default_modified":
            block_x = rect.x + 10 + int(self.w * 0.72 * self.w_scale * 0.9)
            block_y = rect.y + 10 + int(self.h * 0.68 * self.h_scale * 0.8)
            block_w = max(10, int(40 * self.w_scale * 0.9))
            block_h = max(10, int(140 * self.h_scale * 0.8))
            pygame.draw.rect(self.screen, (220, 100, 80), (block_x - block_w // 2, block_y - block_h // 2, block_w, block_h), border_radius=4)

    def _draw_test_results_table(self):
        results = self.repo.get_latest_test_results(limit=100)
        all_results = self.repo.get_test_results()
        
        y_start = 550
        if self.map_buttons:
            y_start = max(y_start, self.map_buttons[-1][0].bottom + 15)

        summary_y = max(430, y_start - 140)
        summary_rect = pygame.Rect(100, summary_y, 1200, 110)
        pygame.draw.rect(self.screen, self.panel_color, summary_rect, border_radius=12)
        pygame.draw.rect(self.screen, (55, 65, 80), summary_rect, 1, border_radius=12)

        title_summary = self.font_subtitle.render("Média de tempo por mapa", True, self.accent)
        self.screen.blit(title_summary, (130, summary_y + 12))

        if not all_results:
            msg = self.font_normal.render("Nenhum teste executado ainda.", True, self.text_sub)
            self.screen.blit(msg, (130, summary_y + 50))
        else:
            summary = summarize_batch_results(all_results)
            total_text = self.font_small.render(f"Execuções acumuladas: {summary['total_executions']}", True, self.text_sub)
            self.screen.blit(total_text, (130, summary_y + 48))

            if summary['by_map']:
                for idx, item in enumerate(summary['by_map']):
                    map_label = str(item['map_name']).replace('_', ' ').title()
                    row_text = (
                        f"{map_label}: {item['average_time']:.2f}s | {item['count']} execs | "
                        f"{item['average_particles_per_second']:.1f} p/s"
                    )
                    lbl = self.font_small.render(row_text, True, self.text_main)
                    self.screen.blit(lbl, (130, summary_y + 72 + idx * 20))

        row_h = 24
        header_h = 45
        visible_h = 200
        
        table_rect = pygame.Rect(100, y_start, 1200, visible_h)
        pygame.draw.rect(self.screen, self.panel_color, table_rect, border_radius=12)
        pygame.draw.rect(self.screen, (55, 65, 80), table_rect, 1, border_radius=12)
        
        title = self.font_subtitle.render("Histórico de Testes (Use o Scroll do Mouse)", True, self.accent)
        self.screen.blit(title, (130, y_start + 12))
        
        y_curr = y_start + header_h
        headers = ["Mapa", "Partículas", "Tempo", "Fluxo", "Status"]
        x_offsets = [130, 380, 600, 820, 1040]
        
        for h, x in zip(headers, x_offsets):
            lbl = self.font_small.render(h, True, self.text_sub)
            self.screen.blit(lbl, (x, y_curr))
            
        y_curr += 20
        pygame.draw.line(self.screen, (55, 65, 80), (130, y_curr), (1270, y_curr), 1)
        
        content_y_start = y_curr + 8
        content_h = visible_h - (content_y_start - y_start) - 10
        
        clip_rect = pygame.Rect(100, content_y_start, 1200, content_h)
        self.screen.set_clip(clip_rect)
        
        total_content_h = len(results) * row_h
        self.max_table_scroll = max(0, total_content_h - content_h)
        self.table_scroll_y = max(-self.max_table_scroll, min(0, self.table_scroll_y))
        
        y_render = content_y_start + self.table_scroll_y
        
        if not results:
            msg = self.font_normal.render("Nenhum teste executado ainda.", True, self.text_sub)
            self.screen.blit(msg, (130, y_render + 4))
            self.screen.set_clip(None)
            return
        
        for i, result in enumerate(results):
            status_text = result.status or 'Concluído'
            
            if i % 2 == 1:
                row_bg = pygame.Rect(115, y_render - 2, 1170, row_h)
                pygame.draw.rect(self.screen, (28, 32, 42), row_bg, border_radius=6)
                
            color = (240, 80, 80) if status_text == 'Não concluído' else (self.success if i == 0 else self.text_main)
            
            texts = [
                str(result.map_name).replace("_", " ").title(),
                f"{result.particles_count} p",
                f"{result.total_time:.2f}s",
                f"{result.particles_per_second:.1f} p/s",
                status_text
            ]
            
            for t, x in zip(texts, x_offsets):
                lbl = self.font_small.render(t, True, color)
                self.screen.blit(lbl, (x, y_render))
            y_render += row_h
            
        self.screen.set_clip(None)
        
        if self.max_table_scroll > 0:
            scroll_bar_bg = pygame.Rect(1280, content_y_start, 6, content_h)
            pygame.draw.rect(self.screen, (40, 45, 55), scroll_bar_bg, border_radius=3)
            
            bar_h = max(15, int((content_h / total_content_h) * content_h))
            scroll_pct = abs(self.table_scroll_y) / self.max_table_scroll
            bar_y = content_y_start + int(scroll_pct * (content_h - bar_h))
            
            scroll_bar = pygame.Rect(1280, bar_y, 6, bar_h)
            pygame.draw.rect(self.screen, self.accent, scroll_bar, border_radius=3)

    def show_results_screen(self):
        self.results_screen.show()

    def _draw_batch_results_table(self, results):
        self.screen.fill(self.bg_color)

        title = self.font_title.render("Resumo Consolidado do Batch", True, self.accent)
        self.screen.blit(title, (title.get_rect(center=(700, 70))))

        summary = summarize_batch_results(results)
        summary_panel = pygame.Rect(70, 130, 1260, 190)
        pygame.draw.rect(self.screen, self.panel_color, summary_panel, border_radius=12)
        pygame.draw.rect(self.screen, (55, 65, 80), summary_panel, 1, border_radius=12)

        summary_title = self.font_subtitle.render("Média de tempo por mapa", True, self.accent)
        self.screen.blit(summary_title, (95, 150))

        if not results:
            msg = self.font_normal.render("Nenhuma execução processada.", True, self.text_sub)
            self.screen.blit(msg, (95, 195))
        else:
            total_text = self.font_small.render(f"Execuções acumuladas: {summary['total_executions']}", True, self.text_sub)
            self.screen.blit(total_text, (95, 190))

            if summary["by_map"]:
                for idx, item in enumerate(summary["by_map"]):
                    map_label = str(item["map_name"]).replace("_", " ").title()
                    row_text = (
                        f"{map_label}: {item['average_time']:.2f}s | {item['count']} execs | "
                        f"{item['average_particles_per_second']:.1f} p/s"
                    )
                    lbl = self.font_small.render(row_text, True, self.text_main)
                    self.screen.blit(lbl, (95, 220 + idx * 24))

        table_rect = pygame.Rect(70, 360, 1260, 330)
        pygame.draw.rect(self.screen, self.panel_color, table_rect, border_radius=12)
        pygame.draw.rect(self.screen, (55, 65, 80), table_rect, 1, border_radius=12)

        headers = ["Execução", "Mapa", "Partículas", "Tempo (s)"]
        x_offsets = [110, 440, 740, 990]
        for header, x in zip(headers, x_offsets):
            lbl = self.font_small.render(header, True, self.text_sub)
            self.screen.blit(lbl, (x, 385))

        pygame.draw.line(self.screen, (60, 70, 85), (110, 410), (1240, 410), 2)

        if not results:
            msg = self.font_normal.render("Nenhuma execução processada.", True, self.text_sub)
            self.screen.blit(msg, (110, 450))
        else:
            y = 435
            for result in results:
                values = [
                    result.execution_name,
                    str(result.map_name).replace("_", " ").title(),
                    str(result.particles_count),
                    f"{result.total_time:.2f}",
                ]
                for value, x in zip(values, x_offsets):
                    lbl = self.font_small.render(value, True, self.text_main)
                    self.screen.blit(lbl, (x, y))
                y += 28

        footer = self.font_subtitle.render("Pressione ESC para voltar ao menu", True, self.text_sub)
        self.screen.blit(footer, (footer.get_rect(center=(700, 720))))

    def show_mode(self):
        running = True
        while running:
            single_btn, batch_btn = self._draw_mode_selection()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "single"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if single_btn.collidepoint(event.pos):
                        return "single"
                    if batch_btn.collidepoint(event.pos):
                        return "batch"

    def show_batch(self):
        return self.batch_menu.show()

    def show_batch_results(self, results):
        return self.batch_menu.show_results(results)

    def get_particle_count(self):
        selecting = True
        while selecting:
            self.screen.fill(self.bg_color)
            
            title = self.font_title.render("AeroSim - Configuração", True, self.text_main)
            self.screen.blit(title, (title.get_rect(center=(700, 200))))

            info = self.font_subtitle.render("Selecione a carga de partículas para o teste:", True, self.text_sub)
            self.screen.blit(info, (info.get_rect(center=(700, 270))))

            for i, count in enumerate(self.count_options):
                btn = self.count_buttons[i]
                is_hover = btn.collidepoint(pygame.mouse.get_pos())
                color = self.hover_color if is_hover else self.panel_color
                
                pygame.draw.rect(self.screen, color, btn, border_radius=10)
                if is_hover:
                    pygame.draw.rect(self.screen, self.accent, btn, 2, border_radius=10)
                    
                label = self.font_normal.render(str(count), True, self.text_main)
                self.screen.blit(label, label.get_rect(center=btn.center))

            pygame.display.flip()

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

        return self.particle_count

    def show(self):
        running = True
        selected_map = None
        change_btn = pygame.Rect(950, 40, 200, 45)
        results_btn = pygame.Rect(1170, 40, 180, 45)

        while running:
            self.screen.fill(self.bg_color)
            mouse_pos = pygame.mouse.get_pos()
            
            title = self.font_title.render("AeroSim", True, self.accent)
            self.screen.blit(title, (100, 40))
            
            subtitle = self.font_subtitle.render("Selecione o mapa para iniciar o escoamento", True, self.text_sub)
            self.screen.blit(subtitle, (100, 95))

            btn_color = self.hover_color if change_btn.collidepoint(mouse_pos) else self.panel_color
            pygame.draw.rect(self.screen, btn_color, change_btn, border_radius=8)
            pygame.draw.rect(self.screen, (60, 70, 85), change_btn, 1, border_radius=8)
            lbl_part = self.font_small.render(f"Carga: {self.particle_count} (Mudar)", True, self.text_main)
            self.screen.blit(lbl_part, lbl_part.get_rect(center=change_btn.center))

            results_color = self.hover_color if results_btn.collidepoint(mouse_pos) else self.panel_color
            pygame.draw.rect(self.screen, results_color, results_btn, border_radius=8)
            pygame.draw.rect(self.screen, (60, 70, 85), results_btn, 1, border_radius=8)
            lbl_results = self.font_small.render("Ver resultados", True, self.text_main)
            self.screen.blit(lbl_results, lbl_results.get_rect(center=results_btn.center))

            for rect, map_name in self.map_buttons:
                is_hover = rect.collidepoint(mouse_pos)
                color = self.hover_color if is_hover else self.panel_color
                
                pygame.draw.rect(self.screen, color, rect, border_radius=12)
                
                border_color = self.accent if is_hover else (60, 70, 85)
                border_width = 2 if is_hover else 1
                pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=12)
                    
                self._draw_preview(map_name, rect)
                
                lbl = self.font_normal.render(map_name.replace("_", " ").title(), True, self.text_main)
                self.screen.blit(lbl, lbl.get_rect(center=(rect.centerx, rect.bottom - 20)))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.table_scroll_y = min(0, self.table_scroll_y + 20)
                    elif event.button == 5:
                        self.table_scroll_y = max(-self.max_table_scroll, self.table_scroll_y - 20)
                    
                    for rect, map_name in self.map_buttons:
                        if rect.collidepoint(mouse_pos):
                            selected_map = map_name
                            running = False
                            break
                    if running and change_btn.collidepoint(mouse_pos):
                        count = self.get_particle_count()
                        if count:
                            self.particle_count = count
                    if running and results_btn.collidepoint(mouse_pos):
                        self.show_results_screen()
                        
            pygame.display.flip()
            
        pygame.quit()
        return selected_map