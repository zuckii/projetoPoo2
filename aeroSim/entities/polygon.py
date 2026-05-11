from aeroSim.entities.obstacle import Obstacle

class Polygon(Obstacle):
    """Polígono simples (retângulo) para obstáculos"""
    
    def __init__(self, x, y, width, height, angle=0):
        """
        x, y: centro do retângulo
        width, height: dimensões
        angle: rotação em graus (opcional)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
    
    def contains(self, px, py) -> bool:
        """Verifica se ponto está dentro do retângulo (AABB simples)"""
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        top = self.y - self.height / 2
        bottom = self.y + self.height / 2
        
        return left <= px <= right and top <= py <= bottom
    
    def get_corners(self) -> list[tuple[float, float]]:
        """Return the four rectangle corners for rendering."""
        half_w = self.width / 2
        half_h = self.height / 2

        return [
            (self.x - half_w, self.y - half_h),
            (self.x + half_w, self.y - half_h),
            (self.x + half_w, self.y + half_h),
            (self.x - half_w, self.y + half_h),
        ]
