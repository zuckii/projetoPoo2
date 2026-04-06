class AeroSolver:
    def __init__(self, model):
        self.model = model

    def step(self, world, dt):
        self.model.solve(world.grid, world.obstacles, dt, particle=world.particle)