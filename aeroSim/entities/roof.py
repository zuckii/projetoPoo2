from aeroSim.entities.obstacle import Obstacle
import math


class Roof(Obstacle):
    """Plano inclinado (telhado) para colisão de partículas"""
    
    def __init__(self, x1, y1, x2, y2):
        """
        Define um plano inclinado com dois pontos
        (x1, y1): ponto inicial (topo)
        (x2, y2): ponto final (base)
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        # Calcular comprimento da linha
        dx = x2 - x1
        dy = y2 - y1
        self.length = math.sqrt(dx*dx + dy*dy)
        
        # Normal perpendicular ao plano (aponta para fora)
        if self.length > 0:
            # Vetor da linha
            self.dir_x = dx / self.length
            self.dir_y = dy / self.length
            
            # Normal perpendicular (rotay 90 graus)
            # Se direção é (dir_x, dir_y), normal é (-dir_y, dir_x)
            self.normal_x = -self.dir_y
            self.normal_y = self.dir_x
        else:
            self.dir_x = 1
            self.dir_y = 0
            self.normal_x = 0
            self.normal_y = 1
    
    def getClosestPoint(self, px, py):
        """Encontra o ponto mais próximo na linha"""
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        
        if self.length == 0:
            return self.x1, self.y1
        
        # Parametro t (0 = inicio, 1 = fim)
        t = ((px - self.x1) * dx + (py - self.y1) * dy) / (self.length * self.length)
        t = max(0, min(1, t))  # Clampar entre 0 e 1
        
        closest_x = self.x1 + t * dx
        closest_y = self.y1 + t * dy
        
        return closest_x, closest_y
    
    def getCorners(self):
        """Retorna os dois pontos da linha (para renderização)"""
        return [(self.x1, self.y1), (self.x2, self.y2)]
    
    def contains(self, px, py) -> bool:
        """Verifica se ponto está dentro (não aplicável para linha, sempre False)"""
        return False
