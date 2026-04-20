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
        
        self.world = World(
            simConfig.GRID_RES, 
            self.engine.screenWidth, 
            self.engine.screenHeight,
            mode=self.mode
        )
        self.solver = AeroSolver(SimpleAeroModel())
        self.renderer = Renderer(self.engine.screenWidth, self.engine.screenHeight, simConfig.GRID_RES)

    def run(self):
        while self.engine.isRunning:
            dt = self.engine.updateTime()
            
            if self.mode == "SANDBOX":
                # SANDBOX: usar stepSandbox
                self.solver.stepSandbox(self.world, dt)
            else:
                # FLUID: usar step normal
                self.solver.step(self.world, dt)
            
            # Atualizar mundo
            self.world.update(dt)
            
            # Renderizar
            self.renderer.render(self.world)