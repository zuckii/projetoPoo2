from aeroSim.environment.fluidGrid import FluidGrid
from aeroSim.environment.obstacleManager import ObstacleManager
from aeroSim.entities.circle import Circle
from aeroSim.entities.particle import Particle

class World:
    def __init__(self, gridRes, screenWidth, screenHeight):
        self.grid = FluidGrid(gridRes)
        self.obstacles = ObstacleManager()
        
        centerX = screenWidth // 2
        centerY = screenHeight // 2
        
        self.obstacles.add(Circle(x=centerX, y=centerY, radius=100))
        self.particle = Particle(x=50, y=centerY, speedX=300.0, speedY=0.0)