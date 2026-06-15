# Simulation settings
FPS_LIMIT = 60  # Target frames per second; adjust for performance vs smoothness

# Physics settings
GRAVITY = 500.0  # pixels/s^2 - downward acceleration for particles
WIND_X = 20.0    # pixels/s^2 - horizontal wind force
WIND_Y = 0.0     # pixels/s^2 - vertical wind force (0 = no vertical wind)
DRAG_COEFFICIENT = 0.99  # velocity multiplier per frame (0.0 = no drag, 1.0 = full drag)
BOUNCE_DAMPING = 0.05  # lower bounce on collisions so sliding feels smoother
PARTICLE_RADIUS = 5.0  # default particle size in pixels