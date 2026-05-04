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
        
        # Força a simulação a ler a resolução NATIVA do seu notebook
        pygame.init()
        info = pygame.display.Info()
        native_w = info.current_w
        native_h = info.current_h
        
        # Alimenta o Mundo e o Renderizador com o tamanho exato da tela
        self.world = World(
            simConfig.GRID_RES, 
            native_w, 
            native_h,
            mode=self.mode
        )
        self.solver = AeroSolver(SimpleAeroModel())
        self.renderer = Renderer(native_w, native_h, simConfig.GRID_RES)

    def run(self):
        while self.engine.isRunning:
            dt = self.engine.updateTime()
            
            if self.mode == "SANDBOX":
                self.solver.stepSandbox(self.world, dt)
            else:
                self.solver.step(self.world, dt)
            
            self.world.update(dt)
            self.renderer.render(self.world)