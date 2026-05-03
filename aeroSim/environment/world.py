from aeroSim.environment.fluidGrid import FluidGrid
from aeroSim.environment.obstacleManager import ObstacleManager
from aeroSim.entities.circle import Circle
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.wedge import Wedge
from aeroSim.entities.roof import Roof
from aeroSim.entities.simplePlatform import SimplePlatform
from aeroSim.entities.particle import Particle
import random
import math

class World:
    def __init__(self, gridRes, screenWidth, screenHeight, mode="SANDBOX"):
        self.grid = FluidGrid(gridRes)
        self.obstacles = ObstacleManager()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.mode = mode
        
        self.particles = []
        self.particle = None
        
        self.spawnTimer = 0.0
        self.spawnInterval = 0.03
        self.spawnActive = False
        
        if mode == "SANDBOX":
            self._initSandbox()
        else:
            self._initFluid()
    
    def _initSandbox(self):
        """Inicializa SANDBOX com 3 plataformas de ponta a ponta e muita inclinação"""
        screen_w = self.screenWidth
        screen_h = self.screenHeight

        wall_thickness = max(20, int(screen_w * 0.02))
        
        # Deixei o buraco com 25% da tela. Isso ajuda a encurtar a plataforma 
        # o suficiente para ela ficar bem íngreme sem perder a estética Donkey Kong.
        ball_gap = int(screen_w * 0.25)  

        # Apenas 3 plataformas para termos espaço de sobra para a inclinação violenta
        n_platforms = 3
        top_margin = screen_h * 0.05
        bottom_margin = screen_h * 0.05
        available_height = screen_h - top_margin - bottom_margin

        vertical_gap = available_height / n_platforms
        
        # A plataforma vai descer 90% de todo o espaço do andar! Muito íngreme.
        dy = vertical_gap * 0.99

        # Paredes laterais para a bolinha não vazar
        self.obstacles.add(Polygon(x=wall_thickness / 2, y=screen_h / 2, width=wall_thickness, height=screen_h))
        self.obstacles.add(Polygon(x=screen_w - wall_thickness / 2, y=screen_h / 2, width=wall_thickness, height=screen_h))

        for i in range(n_platforms):
            y_start = top_margin + (i * vertical_gap)
            y_end = y_start + dy

            if i % 2 == 0:
                # Esquerda para Direita
                x_start = wall_thickness
                x_end = screen_w - ball_gap
            else:
                # Direita para Esquerda
                x_start = screen_w - wall_thickness
                x_end = ball_gap

            self.obstacles.add(Roof(x_start, y_start, x_end, y_end))

        self.spawnActive = True
        self.spawnInterval = 0.03
        self.particles = []

    def spawnParticle(self):
        """Nasce bem no começo da primeiríssima rampa (canto esquerdo)"""
        import random
        
        wall_thickness = max(20, int(self.screenWidth * 0.02))
        
        # Nasce grudadinho na parede esquerda para aproveitar a ladeira inteira
        x = wall_thickness + 30 + random.uniform(-10, 10)
        y = self.screenHeight * 0.02
        
        vx = random.uniform(1, 4)
        vy = 0

        self.particles.append(Particle(x=x, y=y, speedX=vx, speedY=vy, mass=1.0))
    
    def _initFluid(self):
        centerX = self.screenWidth // 2
        centerY = self.screenHeight // 2
        self.obstacles.add(Circle(x=centerX, y=centerY, radius=100))
        self.particle = Particle(x=50, y=centerY, speedX=300.0, speedY=0.0)
    
    def addParticle(self, particle):
        self.particles.append(particle)
    
    def update(self, dt):
        """Atualiza o mundo com geração infinita de partículas"""
        # 1. Matar partículas que caíram no fundo da tela (Limpeza de memória)
        kill_y_threshold = self.screenHeight - 20
        for p in self.particles:
            if p.y > kill_y_threshold:
                p.isAlive = False

        self.particles = [p for p in self.particles if p.isAlive]
        
        # 2. Spawner automático SEM LIMITE (geração contínua)
        if self.spawnActive:
            self.spawnTimer += dt
            while self.spawnTimer >= self.spawnInterval:
                self.spawnParticle()
                self.spawnTimer -= self.spawnInterval
    
    def getAliveParticles(self):
        return [p for p in self.particles if p.isAlive]