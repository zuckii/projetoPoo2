class Particle:
    def __init__(self, x, y, speedX=0.0, speedY=0.0, mass=1.0, radius=5.0):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.vx = speedX  # velocidade em x
        self.vy = speedY  # velocidade em y
        self.mass = mass
        self.radius = radius
        self.isAlive = True

    def updatePosition(self, dt):
        """Atualiza posição baseado em velocidade"""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def applyForce(self, fx, fy, dt):
        """Aplica força (aceleração = força/massa)"""
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * dt
        self.vy += ay * dt
    
    def applyVelocity(self, vx, vy, dt):
        """Aplica velocidade direta (vento, gravidade)"""
        self.vx += vx * dt
        self.vy += vy * dt
    
    def bounce(self, normal_x, normal_y, damping=0.2):
        """Reflete a velocidade separando quique de escorregamento"""
        dot = self.vx * normal_x + self.vy * normal_y
        
        # Só processa se a partícula estiver indo em direção ao obstáculo
        if dot > 0:
            return

        # Componente Normal (o impacto/quique)
        vn_x = dot * normal_x
        vn_y = dot * normal_y
        
        # Componente Tangencial (o escorregamento)
        vt_x = self.vx - vn_x
        vt_y = self.vy - vn_y
        
        # damping atua como "restituição" (quique). 
        # Atrito fixo em 0.01 (muito baixo, escorrega fácil)
        friction = 0.01 
        
        self.vx = (-vn_x * damping) + (vt_x * (1.0 - friction))
        self.vy = (-vn_y * damping) + (vt_y * (1.0 - friction))
    
    def applyDrag(self, drag_coeff):
        """Aplica arrasto à velocidade"""
        self.vx *= drag_coeff
        self.vy *= drag_coeff