from aeroSim.entities.obstacle import Obstacle
import math

class SimplePlatform(Obstacle):
    """Plataforma horizontal simples para colisão de partículas"""
    
    def __init__(self, x1, y, x2):
        """
        Define uma plataforma horizontal
        (x1, y): ponto inicial (esquerda)
        (x2, y): ponto final (direita)
        y: altura da plataforma
        """
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y = y
        
        # Comprimento da plataforma
        self.length = self.x2 - self.x1
        
        # Normal sempre aponta para cima (para plataformas horizontais)
        self.normal_x = 0.0
        self.normal_y = -1.0
    
    def contains(self, px, py) -> bool:
        """Verifica se ponto está dentro da plataforma"""
        # Para uma plataforma horizontal, consideramos uma pequena zona
        tolerance = 10  # 10 pixels acima e abaixo da plataforma
        return self.x1 <= px <= self.x2 and abs(py - self.y) <= tolerance
    
    def getClosestPoint(self, px, py):
        """Encontra o ponto mais próximo na plataforma"""
        # Limitar x ao intervalo da plataforma
        closest_x = max(self.x1, min(px, self.x2))
        closest_y = self.y
        
        return closest_x, closest_y
    
    def getCorners(self):
        """Retorna os dois pontos da plataforma (para renderização)"""
        return [(self.x1, self.y), (self.x2, self.y)]
