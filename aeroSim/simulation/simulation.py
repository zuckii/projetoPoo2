import ctypes
import pygame
import time
from aeroSim.core.engine import Engine
from aeroSim.environment.world import World
from aeroSim.physics.solver import AeroSolver
from aeroSim.graphics.renderer import Renderer
from aeroSim.config import simulationConfig as simConfig
from aeroSim.persistence.repository import PersistenceRepository
class Simulation:
    def __init__(self, map_name: str = "default", test_mode: bool = False, create_renderer: bool = True) -> None:
        self._set_windows_dpi()
        pygame.init()
        try:
            user32 = ctypes.windll.user32
            self.screen_width = user32.GetSystemMetrics(0)
            self.screen_height = user32.GetSystemMetrics(1)
        except Exception:
            display_info = pygame.display.Info()
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
        self.solver = AeroSolver()
        self.renderer = Renderer(self.screen_width, self.screen_height) if create_renderer else None
        self.test_mode = test_mode
        self.repo = PersistenceRepository(preserve_data=True)  # Preserva dados existentes

    def build_runtime(
        self,
        map_name: str,
        particle_count: int | None = None,
        sequence_name: str | None = None,
        gravity: float | None = None,
        wind_x: float | None = None,
        wind_y: float | None = None,
        drag_coefficient: float | None = None,
        bounce_damping: float | None = None,
    ) -> tuple[World, AeroSolver]:
        world = World(
            self.screen_width, 
            self.screen_height, 
            map_name=map_name,
            particle_sequence_name=sequence_name
        )
        if particle_count:
            world.target_particles = particle_count

        solver = AeroSolver(
            gravity=gravity,
            wind_x=wind_x,
            wind_y=wind_y,
            drag_coefficient=drag_coefficient,
            bounce_damping=bounce_damping,
        )
        return world, solver

    def execute_world(
        self,
        world: World,
        solver: AeroSolver,
        execution_name: str,
        map_name: str,
        particles_count: int,
        sequence_name: str | None = None,
        render: bool = True,
        persist_test_result: bool = True,
    ) -> dict:
        engine = Engine(simConfig.FPS_LIMIT)
        started_timing = False
        timing_start = 0.0
        last_particle_exit_time = None
        last_exit_count = 0

        print(f"\n--- Iniciando Execução: {execution_name} ---")
        print(f"Mapa: {map_name}, Partículas: {particles_count}")

        aborted = False
        while engine.is_running and world.particles_exited < world.target_particles:
            dt = engine.update_time()
            solver.step_sandbox(world, dt)
            world.update(dt)
            current_time = time.time()

            if started_timing is False and world.spawned_count > 0:
                started_timing = True
                timing_start = current_time

            if world.particles_exited > last_exit_count:
                last_exit_count = world.particles_exited
                last_particle_exit_time = current_time

            if render:
                if self.renderer is None:
                    self.renderer = Renderer(self.screen_width, self.screen_height)

                if started_timing:
                    elapsed = current_time - timing_start
                    self.renderer.render(world, show_timer=True, elapsed_time=elapsed)
                else:
                    self.renderer.render(world, show_timer=False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        aborted = True
                    engine.is_running = False

            if not engine.is_running:
                break

        end_time = time.time()
        total_time = end_time - timing_start if started_timing else 0.0
        particles_per_second = particles_count / total_time if total_time > 0 else 0.0

        if persist_test_result:
            result_status = 'Não concluído' if aborted else 'Concluído'
            self.repo.save_test_result(
                test_name=execution_name,
                map_name=map_name,
                sequence_name=sequence_name or execution_name,
                total_time=total_time,
                particles_count=particles_count,
                status=result_status,
            )

        result = {
            "test_name": execution_name,
            "sequence_name": sequence_name or execution_name,
            "map_name": map_name,
            "particles_count": particles_count,
            "total_time": total_time,
            "particles_per_second": particles_per_second,
            "status": 'Não concluído' if aborted else 'Concluído',
        }

        print(f"Resultado: Tempo = {total_time:.2f}s | Fluxo = {particles_per_second:.2f} partículas/s | Status = {result['status']}")
        return result

    def _sequence_name_for_count(self, particle_count: int) -> str:
        return f"sequence_count_{particle_count}"

    def run_test(self, map_name: str = "default", particle_count: int = 1000) -> dict:
        """Executa teste com sequência persistente de partículas"""
        from datetime import datetime

        sequence_name = self._sequence_name_for_count(particle_count)
        self.repo.generate_particle_sequence(sequence_name, map_name, particle_count)
        world, solver = self.build_runtime(
            map_name=map_name,
            particle_count=particle_count,
            sequence_name=sequence_name,
        )
        return self.execute_world(
            world=world,
            solver=solver,
            execution_name=f"Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            map_name=map_name,
            particles_count=particle_count,
            sequence_name=sequence_name,
            render=True,
            persist_test_result=True,
        )

    def _set_windows_dpi(self) -> None:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass