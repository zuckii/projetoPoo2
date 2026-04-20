from aeroSim.entities.obstacle import Obstacle
import math

class Wedge(Obstacle):
    """Calha em forma de V com dois planos inclinados convergindo para baixo"""
    
    def __init__(self, x, y, width, height, gap_ratio=0.05):
        """
        x, y: posição do topo da calha (topo-esquerdo ou centro?)
        width: largura total da calha no topo
        height: altura da calha
        gap_ratio: proporção mínima do gap no topo (espaço vazio = width * gap_ratio)
        """
        self.x = x  # Centro
        self.y = y  # Topo
        self.width = width
        self.height = height
        self.gap_ratio = gap_ratio
        
        self.half_width = width / 2
        self.gap_width = width * gap_ratio
        self.half_gap = self.gap_width / 2
    
    def contains(self, px, py) -> bool:
        """Verifica se ponto está DENTRO da calha V (entre os dois planos)"""
        rel_y = py - self.y
        
        # Fora da altura
        if rel_y < 0 or rel_y > self.height:
            return False
        
        # Interpolação linear: no topo tem gap_width, na base converge para 0
        # t = 0 (topo), t = 1 (base)
        t = rel_y / self.height
        
        # Largura em função da profundidade
        # No topo: width
        # Na base: 0 (converge para um ponto)
        current_width = self.half_width * (1.0 - t)
        
        # Não pode ser menor que o gap
        min_half_width = self.half_gap
        if current_width < min_half_width:
            current_width = min_half_width
        
        # Verificar se está entre as paredes
        return -current_width <= (px - self.x) <= current_width
    
    def getCorners(self):
        """Retorna os vértices para renderização (forma de V)"""
        left_top = (self.x - self.half_width, self.y)
        right_top = (self.x + self.half_width, self.y)
        
        left_gap_top = (self.x - self.half_gap, self.y)
        right_gap_top = (self.x + self.half_gap, self.y)
        
        bottom = (self.x, self.y + self.height)
        
        # Retorna em ordem para desenho (polígono)
        return [left_top, left_gap_top, bottom, right_gap_top, right_top]
    
    def getClosestPointOnWall(self, px, py):
        """Encontra o ponto mais próximo nas paredes do V"""
        rel_y = py - self.y
        
        # Clampar à altura
        rel_y = max(0, min(self.height, rel_y))
        
        t = rel_y / self.height
        half_w = self.half_width * (1.0 - t)
        half_w = max(half_w, self.half_gap)
        
        # Determinar qual wall (esquerda ou direita)
        if px - self.x < 0:
            # Parede esquerda: vai de (x - half_width, y) até (x, y + height)
            wall_x = self.x - half_w
        else:
            # Parede direita: vai de (x + half_width, y) até (x, y + height)
            wall_x = self.x + half_w
        
        wall_y = self.y + rel_y
        
        return wall_x, wall_y
    
    def getCollisionNormal(self, px, py):
        """Retorna a normal de colisão (perpendicular à parede)"""
        rel_y = py - self.y
        rel_y = max(0, min(self.height, rel_y))
        
        t = rel_y / self.height
        
        # Ângulo das paredes em relação à vertical
        # tan(angle) = half_width / height
        if self.height > 0:
            tan_angle = self.half_width / self.height
        else:
            tan_angle = 0
        
        if px - self.x < 0:
            # Parede esquerda: normal aponta para fora-esquerda
            # inclinada para cima-direita
            nx = -tan_angle * (1 - t)  # Mais inclinada no topo
            ny = 1.0
        else:
            # Parede direita: normal aponta para fora-direita
            nx = tan_angle * (1 - t)
            ny = 1.0
        
        # Normalizar
        length = math.sqrt(nx*nx + ny*ny)
        if length > 0:
            nx /= length
            ny /= length
        
        return nx, ny
