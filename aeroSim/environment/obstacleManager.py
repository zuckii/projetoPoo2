class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def add(self, obstacle):
        self.obstacles.append(obstacle)

    def getAll(self):
        return self.obstacles