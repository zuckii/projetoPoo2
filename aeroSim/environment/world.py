from aeroSim.environment.fluidGrid import FluidGrid
from aeroSim.environment.obstacleManager import ObstacleManager
from aeroSim.entities.circle import Circle
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.wedge import Wedge
from aeroSim.entities.roof import Roof
from aeroSim.entities.particle import Particle

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
        
        # Obstáculos cinza (círculos)
        self.obstacles.add(Circle(x=centerX, y=centerY, radius=80))
        self.obstacles.add(Circle(x=centerX - 300, y=centerY + 200, radius=60))
        self.obstacles.add(Circle(x=centerX + 300, y=centerY + 200, radius=60))
        
        # Dois telhados inclinados formando um V invertido
        # Telhado esquerdo: do topo-esquerdo até o meio
        roof_top_y = centerY - 150
        roof_middle_y = centerY + 300
        left_x = centerX - 400
        right_x = centerX + 400
        
        self.obstacles.add(Roof(x1=left_x, y1=roof_top_y, x2=centerX, y2=roof_middle_y))
        self.obstacles.add(Roof(x1=right_x, y1=roof_top_y, x2=centerX, y2=roof_middle_y))
        
        # Ativar spawner automático com geração constante e levemente alta
        self.spawnActive = True
        self.spawnInterval = 0.03  # Spawn mais frequente (33 partículas/segundo)
        
        # Criar algumas partículas iniciais (caindo do topo)
        for i in range(10):
            x = 100 + i * (self.screenWidth - 200) // 10
            y = 30 + i * 10
            vx = -50 + i * 10  # velocidade horizontal variada
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
        """Spawn automático de partícula no topo da tela"""
        import random
        x = random.randint(100, self.screenWidth - 100)
        y = 20
        vx = random.uniform(-30, 30)
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