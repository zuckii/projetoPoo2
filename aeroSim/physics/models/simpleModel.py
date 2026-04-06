from aeroSim.physics.models.baseModel import BaseAeroModel

class SimpleAeroModel(BaseAeroModel):
    def solve(self, grid, obstacles, dt, particle=None):
        if particle:
            hasCollision = False
            for obs in obstacles.getAll():
                if obs.contains(particle.x, particle.y):
                    hasCollision = True
                    break
            
            if not hasCollision:
                particle.updatePosition(dt)