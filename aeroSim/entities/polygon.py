from aeroSim.entities.obstacle import Obstacle

class Polygon(Obstacle):
    """Polígono simples (retângulo) para obstáculos"""
    
    def __init__(self, x, y, width, height, angle=0, vx: float = 0.0, vy: float = 0.0,
                 min_x: float | None = None, max_x: float | None = None,
                 min_y: float | None = None, max_y: float | None = None):
        """
        x, y: centro do retângulo
        width, height: dimensões
        angle: rotação em graus (opcional)
        vx, vy: velocidade do retângulo (movimento automático)
        min_x, max_x, min_y, max_y: limites para o movimento
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.vx = vx
        self.vy = vy
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
    
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

    def update(self, dt: float) -> None:
        if self.vx == 0 and self.vy == 0:
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

        half_w = self.width / 2
        half_h = self.height / 2

        if self.min_x is not None and self.x - half_w < self.min_x:
            self.x = self.min_x + half_w
            self.vx = -self.vx
        if self.max_x is not None and self.x + half_w > self.max_x:
            self.x = self.max_x - half_w
            self.vx = -self.vx
        if self.min_y is not None and self.y - half_h < self.min_y:
            self.y = self.min_y + half_h
            self.vy = -self.vy
        if self.max_y is not None and self.y + half_h > self.max_y:
            self.y = self.max_y - half_h
            self.vy = -self.vy
