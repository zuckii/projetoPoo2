class Particle:
    def __init__(self, x, y, speedX, speedY):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY

    def updatePosition(self, dt):
        self.x += self.speedX * dt
        self.y += self.speedY * dt