import pygame
import sys
from aeroSim.graphics.batch_menu import summarize_batch_results

class ResultsScreen:
    def __init__(self, menu):
        self.menu = menu
        self.table_scroll_y = 0
        self.max_table_scroll = 0

    def _draw(self):
        self.menu.screen.fill(self.menu.bg_color)

        title = self.menu.font_title.render("Resultados e Médias Acumuladas", True, self.menu.accent)
        self.menu.screen.blit(title, (title.get_rect(center=(700, 70))))

        back_btn = pygame.Rect(1100, 40, 180, 45)
        mouse_pos = pygame.mouse.get_pos()
        btn_color = self.menu.hover_color if back_btn.collidepoint(mouse_pos) else self.menu.panel_color
        pygame.draw.rect(self.menu.screen, btn_color, back_btn, border_radius=8)
        pygame.draw.rect(self.menu.screen, (60, 70, 85), back_btn, 1, border_radius=8)
        label = self.menu.font_small.render("Voltar", True, self.menu.text_main)
        self.menu.screen.blit(label, label.get_rect(center=back_btn.center))

        results = self.menu.repo.get_latest_test_results(limit=1000)
        all_results = self.menu.repo.get_test_results()

        summary_y = 140
        summary_rect = pygame.Rect(90, summary_y, 1220, 180)
        pygame.draw.rect(self.menu.screen, self.menu.panel_color, summary_rect, border_radius=12)
        pygame.draw.rect(self.menu.screen, (55, 65, 80), summary_rect, 1, border_radius=12)

        summary_title = self.menu.font_subtitle.render("Média de tempo por mapa", True, self.menu.accent)
        self.menu.screen.blit(summary_title, (120, summary_y + 18))

        if not all_results:
            msg = self.menu.font_normal.render("Nenhum teste executado ainda.", True, self.menu.text_sub)
            self.menu.screen.blit(msg, (120, summary_y + 60))
        else:
            summary = summarize_batch_results(all_results)
            total_text = self.menu.font_small.render(f"Execuções acumuladas: {summary['total_executions']}", True, self.menu.text_sub)
            self.menu.screen.blit(total_text, (120, summary_y + 58))

            if summary['by_map']:
                for idx, item in enumerate(summary['by_map']):
                    map_label = str(item['map_name']).replace('_', ' ').title()
                    row_text = (
                        f"{map_label}: {item['average_time']:.2f}s de média por execução | "
                        f"{item['count']} execuções | {item['average_particles_per_second']:.1f} p/s"
                    )
                    lbl = self.menu.font_small.render(row_text, True, self.menu.text_main)
                    self.menu.screen.blit(lbl, (120, summary_y + 88 + idx * 24))

        table_y = 320
        table_rect = pygame.Rect(90, table_y, 1220, 420)
        pygame.draw.rect(self.menu.screen, self.menu.panel_color, table_rect, border_radius=12)
        pygame.draw.rect(self.menu.screen, (55, 65, 80), table_rect, 1, border_radius=12)

        title_table = self.menu.font_subtitle.render("Histórico individual", True, self.menu.accent)
        self.menu.screen.blit(title_table, (120, table_y + 18))

        headers = ["Mapa", "Partículas", "Tempo", "Fluxo", "Status"]
        x_offsets = [130, 380, 600, 820, 1040]
        for header, x in zip(headers, x_offsets):
            lbl = self.menu.font_small.render(header, True, self.menu.text_sub)
            self.menu.screen.blit(lbl, (x, table_y + 55))

        pygame.draw.line(self.menu.screen, (55, 65, 80), (120, table_y + 78), (1280, table_y + 78), 1)

        content_y_start = table_y + 85
        content_h = 340
        row_h = 30
        clip_rect = pygame.Rect(90, content_y_start, 1220, content_h)
        self.menu.screen.set_clip(clip_rect)

        total_content_h = len(results) * row_h
        self.max_table_scroll = max(0, total_content_h - content_h)
        self.table_scroll_y = max(-self.max_table_scroll, min(0, self.table_scroll_y))
        y_render = content_y_start + self.table_scroll_y

        if not results:
            msg = self.menu.font_normal.render("Nenhum teste executado ainda.", True, self.menu.text_sub)
            self.menu.screen.blit(msg, (130, y_render + 4))
            self.menu.screen.set_clip(None)
            return

        for i, result in enumerate(results):
            y_pos = y_render + (i * row_h)
            
            if y_pos + row_h < content_y_start or y_pos > content_y_start + content_h:
                continue

            if i % 2 == 1:
                row_bg = pygame.Rect(100, y_pos - 4, 1200, row_h)
                pygame.draw.rect(self.menu.screen, (28, 32, 42), row_bg, border_radius=6)

            status_text = result.status or 'Concluído'
            color = (240, 80, 80) if status_text == 'Não concluído' else (self.menu.success if i == 0 else self.menu.text_main)
            texts = [
                str(result.map_name).replace("_", " ").title(),
                f"{result.particles_count} p",
                f"{result.total_time:.2f}s",
                f"{result.particles_per_second:.1f} p/s",
                status_text,
            ]
            for text, x in zip(texts, x_offsets):
                lbl = self.menu.font_small.render(text, True, color)
                self.menu.screen.blit(lbl, (x, y_pos))

        self.menu.screen.set_clip(None)

        if self.max_table_scroll > 0:
            scroll_bar_bg = pygame.Rect(1290, content_y_start, 8, content_h)
            pygame.draw.rect(self.menu.screen, (40, 45, 55), scroll_bar_bg, border_radius=4)
            bar_h = max(20, int((content_h / total_content_h) * content_h))
            scroll_pct = abs(self.table_scroll_y) / self.max_table_scroll
            bar_y = content_y_start + int(scroll_pct * (content_h - bar_h))
            scroll_bar = pygame.Rect(1290, bar_y, 8, bar_h)
            pygame.draw.rect(self.menu.screen, self.menu.accent, scroll_bar, border_radius=4)

    def show(self):
        running = True
        while running:
            self._draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEWHEEL:
                    self.table_scroll_y = min(0, max(-self.max_table_scroll, self.table_scroll_y + event.y * 30))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    back_btn = pygame.Rect(1100, 40, 180, 45)

                    if event.button == 4:
                        self.table_scroll_y = min(0, self.table_scroll_y + 30)
                    elif event.button == 5:
                        self.table_scroll_y = max(-self.max_table_scroll, self.table_scroll_y - 30)
                    elif back_btn.collidepoint(mouse_pos):
                        running = False