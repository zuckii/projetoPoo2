from abc import ABC, abstractmethod

class BaseAeroModel(ABC):
    @abstractmethod
    def solve(self, grid, obstacles, dt, particle=None):
        pass