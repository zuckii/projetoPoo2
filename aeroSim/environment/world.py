from aeroSim.environment.fluidGrid import FluidGrid
from aeroSim.environment.obstacleManager import ObstacleManager
from aeroSim.entities.circle import Circle
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.wedge import Wedge
from aeroSim.entities.roof import Roof
from aeroSim.entities.particle import Particle
import random

class World:
    def __init__(self, gridRes, screenWidth, screenHeight, mode="SANDBOX"):
        self.grid = FluidGrid(gridRes)
        self.obstacles = ObstacleManager()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.mode = mode
        
        # Lista de partículas (para SANDBOX)
        self.particles = []
        
        # Partícula única (para compatibilidade com FLUID)
        self.particle = None
        
        # Sistema de spawner automático
        self.spawnTimer = 0.0
        self.spawnInterval = 0.05  # Spawn a cada 0.05 segundos (20 partículas/segundo)
        self.spawnActive = False
        
        if mode == "SANDBOX":
            # SANDBOX: criar ambiente com obstáculos e partículas iniciais
            self._initSandbox()
        else:
            # FLUID: modo original
            self._initFluid()
    
    def _initSandbox(self):
        """Inicializa SANDBOX com obstáculos cinza e telhados inclinados"""
        centerX = self.screenWidth // 2
        centerY = self.screenHeight // 2
        
        # Círculo grande no centro, acima da parte mais estreita do funil
        self.obstacles.add(Circle(x=centerX, y=centerY - 50, radius=80))
        
        # Pinos (círculos menores) abaixo da abertura para as partículas quicarem
        base_y = centerY + 350
        self.obstacles.add(Circle(x=centerX, y=base_y, radius=20))
        self.obstacles.add(Circle(x=centerX - 70, y=base_y + 80, radius=20))
        self.obstacles.add(Circle(x=centerX + 70, y=base_y + 80, radius=20))
        self.obstacles.add(Circle(x=centerX - 140, y=base_y + 160, radius=20))
        self.obstacles.add(Circle(x=centerX, y=base_y + 160, radius=20))
        self.obstacles.add(Circle(x=centerX + 140, y=base_y + 160, radius=20))
        
        # Dois telhados inclinados formando um funil COM ABERTURA REAL
        roof_top_y = centerY - 150
        roof_middle_y = centerY + 250
        gap = 10  # Abertura total de 80 pixels (40 para cada lado do centro)
        
        # Telhado esquerdo para ANTES do centro
        self.obstacles.add(Roof(x1=centerX - 400, y1=roof_top_y, x2=centerX - gap, y2=roof_middle_y))
        # Telhado direito começa DEPOIS do centro
        self.obstacles.add(Roof(x1=centerX + 400, y1=roof_top_y, x2=centerX + gap, y2=roof_middle_y))
        
        # Ativar spawner automático
        self.spawnActive = True
        self.spawnInterval = 0.03  
        
        
        # Criar algumas partículas iniciais centralizadas
        for i in range(15):
            x = centerX + random.uniform(-20, 20)
            y = 30 + random.uniform(-10, 20)
            vx = random.uniform(-15, 15)
            vy = 0
            self.particles.append(Particle(x=x, y=y, speedX=vx, speedY=vy, mass=1.0))
    
    def _initFluid(self):
        """Inicializa FLUID com setup original"""
        centerX = self.screenWidth // 2
        centerY = self.screenHeight // 2
        
        self.obstacles.add(Circle(x=centerX, y=centerY, radius=100))
        self.particle = Particle(x=50, y=centerY, speedX=300.0, speedY=0.0)
    
    def addParticle(self, particle):
        """Adiciona uma partícula ao mundo"""
        self.particles.append(particle)
    
    def spawnParticle(self):
        """Spawn automático de partícula centralizado no topo da tela"""
        import random
        centerX = self.screenWidth // 2
        
        # Centraliza o spawn com uma pequena variação (-20 a 20) para espalhar levemente
        x = centerX + random.uniform(-20, 20)
        y = 20
        
        # Velocidade horizontal baixa para caírem mais retas
        vx = random.uniform(-15, 15)
        vy = 0
        
        self.particles.append(Particle(x=x, y=y, speedX=vx, speedY=vy, mass=1.0))
    
    def update(self, dt):
        """Atualiza o mundo (partículas que ainda estão vivas)"""
        # Remover partículas que saíram da tela
        self.particles = [p for p in self.particles if p.isAlive]
        
        # Spawner automático
        if self.spawnActive:
            self.spawnTimer += dt
            while self.spawnTimer >= self.spawnInterval:
                self.spawnParticle()
                self.spawnTimer -= self.spawnInterval
    
    def getAliveParticles(self):
        """Retorna partículas vivas"""
        return [p for p in self.particles if p.isAlive]