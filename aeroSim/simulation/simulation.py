import ctypes
import pygame
from aeroSim.core.engine import Engine
from aeroSim.environment.world import World
from aeroSim.physics.solver import AeroSolver
from aeroSim.physics.models.simpleModel import SimpleAeroModel
from aeroSim.graphics.renderer import Renderer
from aeroSim.config import simulationConfig as simConfig

class Simulation:
    def __init__(self):
        self.engine = Engine(simConfig.FPS_LIMIT)
        self.mode = simConfig.SIMULATION_MODE
        
        # Desliga a mentira de Escala do Windows
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass
        
        pygame.init()
        
        # Abre a tela fullscreen primeiro para medir
        temp_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        real_w = temp_screen.get_width()
        real_h = temp_screen.get_height()
        
        # Repassa as dimensões verdadeiras para o Mundo
        self.world = World(
            simConfig.GRID_RES, 
            real_w, 
            real_h,
            mode=self.mode
        )
        self.solver = AeroSolver(SimpleAeroModel())
        self.renderer = Renderer(real_w, real_h, simConfig.GRID_RES)

    def run(self):
        while self.engine.isRunning:
            dt = self.engine.updateTime()
            
            if self.mode == "SANDBOX":
                self.solver.stepSandbox(self.world, dt)
            else:
                self.solver.step(self.world, dt)
            
            self.world.update(dt)
            self.renderer.render(self.world)