import numpy as np
from aeroSim.config import physicsConfig as physConfig

class FluidGrid:
    def __init__(self, resolution):
        self.res = resolution
        self.u = np.full((resolution, resolution), physConfig.BASE_WIND_SPEED)
        self.v = np.zeros((resolution, resolution))