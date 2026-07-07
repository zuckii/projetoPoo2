import pygame
import sys
from aeroSim.simulation.batchRunner import BatchExecutionConfig


def summarize_batch_results(results):
    if not results:
        return {
            "total_executions": 0,
            "overall_avg_time": 0.0,
            "overall_avg_particles_per_second": 0.0,
            "by_map": [],
        }

    grouped = {}
    total_time = 0.0
    total_particles = 0

    for result in results:
        total_time += result.total_time
        total_particles += result.particles_count

        bucket = grouped.setdefault(
            result.map_name,
            {
                "map_name": result.map_name,
                "count": 0,
                "total_time": 0.0,
                "particles_count": 0,
            },
        )
        bucket["count"] += 1
        bucket["total_time"] += result.total_time
        bucket["particles_count"] += result.particles_count

    overall_avg_time = total_time / len(results)
    overall_avg_particles_per_second = (
        total_particles / overall_avg_time if overall_avg_time > 0 else 0.0
    )

    by_map = []
    for _, bucket in grouped.items():
        avg_time = bucket["total_time"] / bucket["count"]
        avg_particles_per_second = (
            bucket["particles_count"] / avg_time if avg_time > 0 else 0.0
        )
        by_map.append(
            {
                "map_name": bucket["map_name"],
                "count": bucket["count"],
                "average_time": avg_time,
                "average_particles_per_second": avg_particles_per_second,
            }
        )

    by_map.sort(key=lambda item: item["map_name"])
    return {
        "total_executions": len(results),
        "overall_avg_time": overall_avg_time,
        "overall_avg_particles_per_second": overall_avg_particles_per_second,
        "by_map": by_map,
    }


class BatchMenu:
    def __init__(self, main_menu):
        self.menu = main_menu
        self.queue = []
        self.selected_particles = self.menu.particle_count
        self.card_w = 280
        self.card_h = 160
        self.map_buttons = self._build_map_buttons()

    def _build_map_buttons(self):
        buttons = []
        columns = 3
        gap_x = 25
        gap_y = 25
        start_x = 50
        start_y = 150

        for index, map_name in enumerate(self.menu.map_names):
            column = index % columns
            row = index // columns
            x = start_x + column * (self.card_w + gap_x)
            y = start_y + row * (self.card_h + gap_y)
            rect = pygame.Rect(x, y, self.card_w, self.card_h)
            buttons.append((rect, map_name))
        return buttons

    def show(self):
        running = True
        sidebar_rect = pygame.Rect(1000, 40, 350, 720)
        run_btn = pygame.Rect(1020, 680, 310, 50)
        clear_btn = pygame.Rect(1020, 620, 145, 45)
        back_btn = pygame.Rect(1185, 620, 145, 45)

        while running:
            self.menu.screen.fill(self.menu.bg_color)
            mouse_pos = pygame.mouse.get_pos()

            title = self.menu.font_title.render("AeroSim - Configuração de Batch", True, self.menu.accent)
            self.menu.screen.blit(title, (50, 40))

            subtitle = self.menu.font_subtitle.render("Selecione os mapas para adicionar à fila", True, self.menu.text_sub)
            self.menu.screen.blit(subtitle, (50, 90))

            pygame.draw.rect(self.menu.screen, self.menu.panel_color, sidebar_rect, border_radius=12)

            sidebar_title = self.menu.font_subtitle.render("Fila de Execução", True, self.menu.text_main)
            self.menu.screen.blit(sidebar_title, (1020, 60))

            y = 100
            if not self.queue:
                msg = self.menu.font_small.render("Fila vazia.", True, self.menu.text_sub)
                self.menu.screen.blit(msg, (1020, y))
            else:
                for idx, item in enumerate(self.queue[-16:]):
                    lbl = self.menu.font_small.render(f"{idx+1}. {item.map_name} ({item.particles_count}p)", True, self.menu.text_main)
                    self.menu.screen.blit(lbl, (1020, y))
                    y += 24

            part_title = self.menu.font_normal.render("Partículas:", True, self.menu.text_main)
            self.menu.screen.blit(part_title, (1020, 510))

            btn_w = 55
            for i, count in enumerate(self.menu.count_options):
                btn_rect = pygame.Rect(1020 + (i * (btn_w + 7)), 540, btn_w, 35)
                is_hover = btn_rect.collidepoint(mouse_pos)
                color = self.menu.accent if count == self.selected_particles else (self.menu.hover_color if is_hover else self.menu.bg_color)
                pygame.draw.rect(self.menu.screen, color, btn_rect, border_radius=6)
                lbl = self.menu.font_small.render(str(count), True, self.menu.text_main)
                self.menu.screen.blit(lbl, lbl.get_rect(center=btn_rect.center))

            for btn, label, color in [(run_btn, "Iniciar Batch", (50, 160, 100)), (clear_btn, "Limpar", self.menu.hover_color), (back_btn, "Voltar", self.menu.hover_color)]:
                is_hover = btn.collidepoint(mouse_pos)
                bg = self.menu.accent if is_hover and btn == run_btn else (self.menu.panel_color if not is_hover else (80, 90, 105))
                pygame.draw.rect(self.menu.screen, bg if btn != run_btn else color, btn, border_radius=8)
                pygame.draw.rect(self.menu.screen, self.menu.text_sub, btn, 1, border_radius=8)
                text = self.menu.font_normal.render(label, True, self.menu.text_main)
                self.menu.screen.blit(text, text.get_rect(center=btn.center))

            for rect, map_name in self.map_buttons:
                is_hover = rect.collidepoint(mouse_pos)
                color = self.menu.hover_color if is_hover else self.menu.panel_color
                pygame.draw.rect(self.menu.screen, color, rect, border_radius=12)
                border = self.menu.accent if is_hover else (60, 70, 85)
                pygame.draw.rect(self.menu.screen, border, rect, 2 if is_hover else 1, border_radius=12)
                
                old_scale = (self.menu.w_scale, self.menu.h_scale)
                self.menu.w_scale = self.card_w / self.menu.w
                self.menu.h_scale = self.card_h / self.menu.h
                self.menu._draw_preview(map_name, rect)
                self.menu.w_scale, self.menu.h_scale = old_scale
                
                lbl = self.menu.font_normal.render(map_name.replace("_", " ").title(), True, self.menu.text_main)
                self.menu.screen.blit(lbl, lbl.get_rect(center=(rect.centerx, rect.bottom - 20)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if run_btn.collidepoint(event.pos):
                        return self.queue
                    if clear_btn.collidepoint(event.pos):
                        self.queue.clear()
                    if back_btn.collidepoint(event.pos):
                        return None

                    for i, count in enumerate(self.menu.count_options):
                        btn_rect = pygame.Rect(1020 + (i * (btn_w + 7)), 540, btn_w, 35)
                        if btn_rect.collidepoint(event.pos):
                            self.selected_particles = count

                    for rect, map_name in self.map_buttons:
                        if rect.collidepoint(event.pos):
                            execution_name = f"{map_name}_{len(self.queue) + 1}"
                            self.queue.append(BatchExecutionConfig(
                                execution_name=execution_name,
                                map_name=map_name,
                                particles_count=self.selected_particles,
                            ))
                            break

    def show_results(self, results):
        running = True
        while running:
            self.menu._draw_batch_results_table(results)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

        pygame.quit()
        return results