from aeroSim.core.engine import Engine
from aeroSim.environment.world import World
from aeroSim.physics.solver import AeroSolver
from aeroSim.physics.models.simpleModel import SimpleAeroModel
from aeroSim.graphics.renderer import Renderer
from aeroSim.config import simulationConfig as simConfig

class Simulation:
    def __init__(self):
        self.engine = Engine(simConfig.FPS_LIMIT)
        
        self.world = World(simConfig.GRID_RES, self.engine.screenWidth, self.engine.screenHeight)
        self.solver = AeroSolver(SimpleAeroModel())
        self.renderer = Renderer(self.engine.screenWidth, self.engine.screenHeight, simConfig.GRID_RES)

    def run(self):
        while self.engine.isRunning:
            dt = self.engine.updateTime()
            self.solver.step(self.world, dt)
            self.renderer.render(self.world)