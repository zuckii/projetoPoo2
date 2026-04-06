from abc import ABC, abstractmethod

class Obstacle(ABC):
    @abstractmethod
    def contains(self, x, y) -> bool:
        pass