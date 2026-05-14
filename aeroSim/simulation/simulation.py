import ctypes
import pygame
from aeroSim.core.engine import Engine
from aeroSim.environment.world import World
from aeroSim.physics.solver import AeroSolver
from aeroSim.graphics.renderer import Renderer
from aeroSim.config import simulationConfig as simConfig

class Simulation:
    def __init__(self, map_name: str = "default") -> None:
        self._set_windows_dpi()

        pygame.init()
        self.engine = Engine(simConfig.FPS_LIMIT)

        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h

        self.world = World(
            self.screen_width,
            self.screen_height,
            map_name=map_name
        )
        self.solver = AeroSolver()
        self.renderer = Renderer(self.screen_width, self.screen_height)

    def run(self) -> None:
        while self.engine.is_running:
            dt = self.engine.update_time()

            self.solver.step_sandbox(self.world, dt)

            self.world.update(dt)
            self.renderer.render(self.world)

    def _set_windows_dpi(self) -> None:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass