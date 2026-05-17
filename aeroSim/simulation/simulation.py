import ctypes
import pygame
import time
from datetime import datetime
from aeroSim.core.engine import Engine
from aeroSim.environment.world import World
from aeroSim.physics.solver import AeroSolver
from aeroSim.graphics.renderer import Renderer
from aeroSim.config import simulationConfig as simConfig
from aeroSim.persistence.repository import PersistenceRepository

class Simulation:
    def __init__(self, map_name: str = "default", test_mode: bool = False) -> None:
        self._set_windows_dpi()
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.solver = AeroSolver()
        self.renderer = Renderer(self.screen_width, self.screen_height)
        self.test_mode = test_mode
        self.repo = PersistenceRepository(preserve_data=True)  # Preserva dados existentes

    def _setup_world(self, map_name: str, particle_count: int = None, particle_sequence_name: str = None):
        self.engine = Engine(simConfig.FPS_LIMIT)
        self.world = World(
            self.screen_width, 
            self.screen_height, 
            map_name=map_name,
            particle_sequence_name=particle_sequence_name
        )
        if particle_count:
            self.world.target_particles = particle_count

    def run_test(self, map_name: str = "default", particle_count: int = 1000) -> dict:
        """Executa teste com sequência persistente de partículas"""
        # Gera sequência persistente
        sequence_name = f"{map_name}_seq_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.repo.generate_particle_sequence(sequence_name, map_name, particle_count)
        
        # Configura mundo para teste com a sequência
        self._setup_world(map_name, particle_count, sequence_name)
        
        # Executa simulação
        start_time = time.time()
        started_timing = False
        timing_start = 0.0
        last_particle_exit_time = None
        last_exit_count = 0
        timeout_seconds = 30
        
        print(f"\n--- Iniciando Teste: {sequence_name} ---")
        print(f"Mapa: {map_name}, Partículas: {particle_count}")
        
        timeout_status = 'Concluído'
        aborted = False
        while self.engine.is_running and self.world.particles_exited < self.world.target_particles:
            dt = self.engine.update_time()
            self.solver.step_sandbox(self.world, dt)
            self.world.update(dt)
            current_time = time.time()

            # Inicia cronômetro quando a primeira partícula é gerada
            if self.world.spawned_count > 0 and not started_timing:
                started_timing = True
                timing_start = current_time

            # Atualiza o timer de inatividade a partir da primeira queda
            if self.world.particles_exited > last_exit_count:
                last_exit_count = self.world.particles_exited
                last_particle_exit_time = current_time

            # Renderiza com cronômetro
            if started_timing:
                elapsed = current_time - timing_start
                self.renderer.render(self.world, show_timer=True, elapsed_time=elapsed)
            else:
                self.renderer.render(self.world, show_timer=False)

            # Verifica timeout (30 segundos sem queda)
            if last_particle_exit_time is not None:
                time_since_last_exit = current_time - last_particle_exit_time
                if time_since_last_exit > timeout_seconds:
                    print(f"Timeout: Nenhuma partícula caiu por {timeout_seconds}s")
                    timeout_status = 'Não concluído'
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Marcar abortado quando o usuário pressionar ESC
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        aborted = True
                    self.engine.is_running = False

            if not self.engine.is_running:
                break

        end_time = time.time()
        total_time = end_time - timing_start if started_timing else 0
        particles_per_second = particle_count / total_time if total_time > 0 else 0
        
        # Salva resultado
        test_name = f"Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if 'timeout_status' in locals() and timeout_status == 'Não concluído':
            result_status = 'Não concluído'
        elif aborted:
            result_status = 'Não concluído'
        else:
            result_status = 'Concluído'
        self.repo.save_test_result(
            test_name=test_name,
            map_name=map_name,
            sequence_name=sequence_name,
            total_time=total_time,
            particles_count=particle_count,
            status=result_status
        )
        
        result = {
            "test_name": test_name,
            "sequence_name": sequence_name,
            "map_name": map_name,
            "particles_count": particle_count,
            "total_time": total_time,
            "particles_per_second": particles_per_second,
            "status": result_status
        }
        
        print(f"Resultado: Tempo = {total_time:.2f}s | Fluxo = {particles_per_second:.2f} partículas/s | Status = {result_status}")
        
        return result

    def _set_windows_dpi(self) -> None:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass