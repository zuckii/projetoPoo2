from aeroSim.config import physicsConfig as physConfig


class FluidGrid:
    def __init__(self, resolution: int) -> None:
        self.resolution = resolution

    def get_wind_at_position(self, x: float, y: float, screen_width: int, screen_height: int) -> tuple[float, float]:
        return physConfig.WIND_X, physConfig.WIND_Y