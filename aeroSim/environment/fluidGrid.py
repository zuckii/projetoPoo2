import numpy as np
from aeroSim.config import physicsConfig as physConfig

class FluidGrid:
    def __init__(self, resolution):
        self.res = resolution
        self.u = np.full((resolution, resolution), physConfig.BASE_WIND_SPEED)
        self.v = np.zeros((resolution, resolution))
    
    def getWindAtPosition(self, x, y, screen_width, screen_height):
        """
        Retorna velocidade de vento em uma posição específica.
        Para SANDBOX, retorna vento constante.
        """
        return physConfig.WIND_X, physConfig.WIND_Y
    
    def getwindVelocity(self):
        """Retorna velocidade de vento constante para SANDBOX"""
        return physConfig.WIND_X, physConfig.WIND_Y