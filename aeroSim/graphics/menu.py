import pygame
import sys
import ctypes
from aeroSim.persistence.repository import PersistenceRepository
from aeroSim.simulation.batchRunner import BatchExecutionConfig

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
        
        # Escala dinâmica baseada no tamanho do card
        self.card_w = 360
        self.card_h = 180
        self.w_scale = self.card_w / self.w
        self.h_scale = self.card_h / self.h

        # Paleta de Cores
        self.bg_color = (20, 22, 28)
        self.panel_color = (35, 40, 50)
        self.hover_color = (45, 55, 70)
        self.text_main = (250, 250, 255)
        self.text_sub = (170, 180, 190)
        self.accent = (60, 150, 255)
        self.success = (80, 220, 120)

        self.map_names = self.repo.get_map_names()
        self.map_buttons = self._build_map_buttons()

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
        
        # Fundo do preview para destacar o mapa
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
            pygame.draw.rect(
                self.screen,
                (220, 100, 80),
                (block_x - block_w // 2, block_y - block_h // 2, block_w, block_h),
                border_radius=4
            )

    def _draw_test_results_table(self):
        results = self.repo.get_latest_test_results(limit=5)
        
        # Posição dinâmica baseada nos cards
        y_offset = 600
        if self.map_buttons:
            y_offset = max(y_offset, self.map_buttons[-1][0].bottom + 40)
            
        table_rect = pygame.Rect(100, y_offset, 1200, 180)
        pygame.draw.rect(self.screen, self.panel_color, table_rect, border_radius=12)
        
        title = self.font_subtitle.render("Últimos Testes de Vazão", True, self.text_main)
        self.screen.blit(title, (130, y_offset + 15))
        
        y_offset += 60
        headers = ["Mapa", "Partículas", "Tempo (s)", "Fluxo (p/s)", "Status"]
        x_offsets = [130, 350, 550, 750, 950]
        
        for h, x in zip(headers, x_offsets):
            lbl = self.font_small.render(h, True, self.text_sub)
            self.screen.blit(lbl, (x, y_offset))
            
        y_offset += 25
        pygame.draw.line(self.screen, (60, 70, 85), (130, y_offset), (1260, y_offset), 2)
        y_offset += 15
        
        if not results:
            msg = self.font_normal.render("Nenhum teste executado ainda.", True, self.text_sub)
            self.screen.blit(msg, (130, y_offset + 10))
            return
        
        for i, result in enumerate(results):
            status_text = result.status or 'Concluído'
            color = (240, 80, 80) if status_text == 'Não concluído' else (self.success if i == 0 else self.text_main)
            
            texts = [
                str(result.map_name).replace("_", " ").title(),
                str(result.particles_count),
                f"{result.total_time:.2f}s",
                f"{result.particles_per_second:.1f}",
                status_text
            ]
            
            for t, x in zip(texts, x_offsets):
                lbl = self.font_small.render(t, True, color)
                self.screen.blit(lbl, (x, y_offset))
            y_offset += 22

    def _draw_batch_queue(self, queue, panel_rect):
        pygame.draw.rect(self.screen, self.panel_color, panel_rect, border_radius=12)
        title = self.font_subtitle.render("Fila do Batch", True, self.text_main)
        self.screen.blit(title, (panel_rect.x + 20, panel_rect.y + 15))

        y = panel_rect.y + 60
        if not queue:
            msg = self.font_small.render("Nenhuma execução adicionada.", True, self.text_sub)
            self.screen.blit(msg, (panel_rect.x + 20, y))
            return

        for index, item in enumerate(queue[-8:], start=max(1, len(queue) - 7)):
            line = f"{index}. {item.execution_name} | {item.map_name} | {item.particles_count}"
            lbl = self.font_small.render(line, True, self.text_main)
            self.screen.blit(lbl, (panel_rect.x + 20, y))
            y += 24

    def _draw_batch_results_table(self, results):
        self.screen.fill(self.bg_color)

        title = self.font_title.render("Resumo Consolidado do Batch", True, self.accent)
        self.screen.blit(title, (title.get_rect(center=(700, 80))))

        table_rect = pygame.Rect(70, 150, 1260, 520)
        pygame.draw.rect(self.screen, self.panel_color, table_rect, border_radius=12)

        headers = ["Execução", "Mapa", "Partículas", "Tempo (s)"]
        x_offsets = [110, 460, 760, 980]
        for header, x in zip(headers, x_offsets):
            lbl = self.font_small.render(header, True, self.text_sub)
            self.screen.blit(lbl, (x, 185))

        pygame.draw.line(self.screen, (60, 70, 85), (110, 210), (1240, 210), 2)

        if not results:
            msg = self.font_normal.render("Nenhuma execução foi processada.", True, self.text_sub)
            self.screen.blit(msg, (110, 250))
            return

        y = 235
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
        running = True
        queue: list[BatchExecutionConfig] = []
        selected_particles = self.particle_count
        run_btn = pygame.Rect(1120, 40, 180, 45)
        clear_btn = pygame.Rect(1120, 95, 180, 45)
        back_btn = pygame.Rect(1120, 150, 180, 45)
        batch_panel = pygame.Rect(930, 230, 330, 470)

        while running:
            self.screen.fill(self.bg_color)
            mouse_pos = pygame.mouse.get_pos()

            title = self.font_title.render("AeroSim - Batch", True, self.accent)
            self.screen.blit(title, (100, 40))

            subtitle = self.font_subtitle.render("Adicione várias execuções antes de iniciar a sequência", True, self.text_sub)
            self.screen.blit(subtitle, (100, 95))

            buttons = [
                (run_btn, "Executar"),
                (clear_btn, "Limpar fila"),
                (back_btn, "Voltar"),
            ]
            for rect, label in buttons:
                color = self.hover_color if rect.collidepoint(mouse_pos) else self.panel_color
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                pygame.draw.rect(self.screen, (60, 70, 85), rect, 1, border_radius=8)
                lbl = self.font_small.render(label, True, self.text_main)
                self.screen.blit(lbl, lbl.get_rect(center=rect.center))

            selected_count_text = self.font_small.render(f"Partículas por execução: {selected_particles}", True, self.text_main)
            self.screen.blit(selected_count_text, (100, 270))
            for i, count in enumerate(self.count_options):
                btn = self.count_buttons[i]
                is_hover = btn.collidepoint(mouse_pos)
                color = self.accent if count == selected_particles else (self.hover_color if is_hover else self.panel_color)
                pygame.draw.rect(self.screen, color, btn, border_radius=10)
                label = self.font_small.render(str(count), True, self.text_main)
                self.screen.blit(label, label.get_rect(center=btn.center))

            for rect, map_name in self.map_buttons:
                is_hover = rect.collidepoint(mouse_pos)
                color = self.hover_color if is_hover else self.panel_color
                pygame.draw.rect(self.screen, color, rect, border_radius=12)
                border_color = self.accent if is_hover else (60, 70, 85)
                pygame.draw.rect(self.screen, border_color, rect, 2 if is_hover else 1, border_radius=12)
                self._draw_preview(map_name, rect)
                lbl = self.font_normal.render(map_name.replace("_", " ").title(), True, self.text_main)
                self.screen.blit(lbl, lbl.get_rect(center=(rect.centerx, rect.bottom - 20)))

            self._draw_batch_queue(queue, batch_panel)

            queue_hint = self.font_small.render("Clique em um mapa para adicionar a execução atual à fila.", True, self.text_sub)
            self.screen.blit(queue_hint, (930, 715))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if run_btn.collidepoint(event.pos):
                        return queue
                    if clear_btn.collidepoint(event.pos):
                        queue.clear()
                        continue
                    if back_btn.collidepoint(event.pos):
                        return None

                    for i, count in enumerate(self.count_options):
                        if self.count_buttons[i].collidepoint(event.pos):
                            selected_particles = count
                            break

                    for rect, map_name in self.map_buttons:
                        if rect.collidepoint(event.pos):
                            execution_name = f"{map_name}_{len(queue) + 1}"
                            queue.append(BatchExecutionConfig(
                                execution_name=execution_name,
                                map_name=map_name,
                                particles_count=selected_particles,
                            ))
                            break

    def show_batch_results(self, results):
        running = True
        while running:
            self._draw_batch_results_table(results)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

        pygame.quit()
        return results

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
        change_btn = pygame.Rect(1150, 40, 200, 45)

        while running:
            self.screen.fill(self.bg_color)
            mouse_pos = pygame.mouse.get_pos()
            
            # Cabeçalho
            title = self.font_title.render("AeroSim", True, self.accent)
            self.screen.blit(title, (100, 40))
            
            subtitle = self.font_subtitle.render("Selecione o mapa para iniciar o escoamento", True, self.text_sub)
            self.screen.blit(subtitle, (100, 95))

            # Botão de alteração de partículas
            btn_color = self.hover_color if change_btn.collidepoint(mouse_pos) else self.panel_color
            pygame.draw.rect(self.screen, btn_color, change_btn, border_radius=8)
            pygame.draw.rect(self.screen, (60, 70, 85), change_btn, 1, border_radius=8)
            lbl_part = self.font_small.render(f"Carga: {self.particle_count} (Mudar)", True, self.text_main)
            self.screen.blit(lbl_part, lbl_part.get_rect(center=change_btn.center))

            # Renderização dos Cards
            for rect, map_name in self.map_buttons:
                is_hover = rect.collidepoint(mouse_pos)
                color = self.hover_color if is_hover else self.panel_color
                
                pygame.draw.rect(self.screen, color, rect, border_radius=12)
                
                # Borda de destaque
                border_color = self.accent if is_hover else (60, 70, 85)
                border_width = 2 if is_hover else 1
                pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=12)
                    
                self._draw_preview(map_name, rect)
                
                lbl = self.font_normal.render(map_name.replace("_", " ").title(), True, self.text_main)
                self.screen.blit(lbl, lbl.get_rect(center=(rect.centerx, rect.bottom - 20)))
            
            self._draw_test_results_table()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, map_name in self.map_buttons:
                        if rect.collidepoint(mouse_pos):
                            selected_map = map_name
                            running = False
                            break
                    if running and change_btn.collidepoint(mouse_pos):
                        count = self.get_particle_count()
                        if count:
                            self.particle_count = count
                        
            pygame.display.flip()
            
        pygame.quit()
        return selected_map