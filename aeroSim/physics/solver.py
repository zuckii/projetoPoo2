import math
from aeroSim.config import physicsConfig as physConfig
from aeroSim.entities.polygon import Polygon
from aeroSim.entities.roof import Roof

class AeroSolver:

    def step_sandbox(self, world, dt: float) -> None:
        particles = world.get_alive_particles()
        if not particles:
            return

        sub_steps = 4
        sub_dt = dt / sub_steps

        for _ in range(sub_steps):
            for particle in particles:
                particle.apply_acceleration(0.0, physConfig.GRAVITY, sub_dt)
                particle.update_position(sub_dt)
                self._check_bounds(particle, world)

            self._check_particle_collisions(particles)

            for particle in particles:
                self._check_obstacle_collisions(particle, world)

    def _check_obstacle_collisions(self, particle, world) -> None:
        for obs in world.obstacles:
            if isinstance(obs, Polygon):
                self._resolve_polygon_collision(particle, obs)
            elif isinstance(obs, Roof):
                self._resolve_roof_collision(particle, obs)

    def _check_particle_collisions(self, particles) -> None:
        if not particles:
            return

        cell_size = 15.0
        grid: dict[tuple[int, int], list] = {}

        for p in particles:
            cell = (int(p.x // cell_size), int(p.y // cell_size))
            grid.setdefault(cell, []).append(p)

        checked_pairs: set[tuple[int, int]] = set()

        for cell, cell_particles in grid.items():
            cx, cy = cell
            neighbors = [
                (cx - 1, cy - 1), (cx, cy - 1), (cx + 1, cy - 1),
                (cx - 1, cy),     (cx, cy),     (cx + 1, cy),
                (cx - 1, cy + 1), (cx, cy + 1), (cx + 1, cy + 1),
            ]

            for neighbor in neighbors:
                if neighbor not in grid:
                    continue

                for p1 in cell_particles:
                    for p2 in grid[neighbor]:
                        if p1 is p2:
                            continue

                        pair_id = tuple(sorted((id(p1), id(p2))))
                        if pair_id in checked_pairs:
                            continue
                        checked_pairs.add(pair_id)

                        dx = p2.x - p1.x
                        dy = p2.y - p1.y
                        dist_sq = dx * dx + dy * dy
                        min_dist = p1.radius + p2.radius

                        if dist_sq < min_dist * min_dist and dist_sq > 1e-4:
                            dist = math.sqrt(dist_sq)
                            nx = dx / dist
                            ny = dy / dist

                            overlap = min_dist - dist
                            separation = overlap * 0.5

                            p1.x -= nx * separation
                            p1.y -= ny * separation
                            p2.x += nx * separation
                            p2.y += ny * separation

                            dvx = p2.vx - p1.vx
                            dvy = p2.vy - p1.vy
                            dvn = dvx * nx + dvy * ny

                            if dvn < 0:
                                damping = physConfig.BOUNCE_DAMPING if dvn < -15.0 else 0.0
                                impulse = -(1 + damping) * dvn / (1 / p1.mass + 1 / p2.mass)
                                p1.vx -= impulse * nx / p1.mass
                                p1.vy -= impulse * ny / p1.mass
                                p2.vx += impulse * nx / p2.mass
                                p2.vy += impulse * ny / p2.mass

    def _resolve_polygon_collision(self, particle, obs) -> None:
        half_w = obs.width / 2
        half_h = obs.height / 2

        left = obs.x - half_w
        right = obs.x + half_w
        top = obs.y - half_h
        bottom = obs.y + half_h

        closest_x = max(left, min(particle.x, right))
        closest_y = max(top, min(particle.y, bottom))

        dx = particle.x - closest_x
        dy = particle.y - closest_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < particle.radius:
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                nx = 1.0 if abs(dx) > abs(dy) and dx > 0 else -1.0 if abs(dx) > abs(dy) else 0.0
                ny = 0.0 if abs(dx) > abs(dy) else (1.0 if dy > 0 else -1.0)

            overlap = particle.radius - dist
            particle.x += nx * overlap
            particle.y += ny * overlap
            particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING if abs(particle.vy) > 15.0 else 0.0)

    def _resolve_roof_collision(self, particle, roof) -> None:
        cx, cy = roof.get_closest_point(particle.x, particle.y)
        dx = particle.x - cx
        dy = particle.y - cy
        dist_sq = dx * dx + dy * dy

        if dist_sq < particle.radius * particle.radius:
            dist = math.sqrt(dist_sq) if dist_sq > 0 else 0.1
            nx, ny = roof.normal_x, roof.normal_y
            
            if dx * nx + dy * ny < 0:
                nx, ny = -nx, -ny

            overlap = particle.radius - dist
            if overlap > 0:
                particle.x += nx * overlap
                particle.y += ny * overlap
                particle.bounce(nx, ny, physConfig.BOUNCE_DAMPING if abs(particle.vy) > 15.0 else 0.0)

    def _check_bounds(self, particle, world) -> None:
        margin = 100
        if (
            particle.x < -margin
            or particle.x > world.screen_width + margin
            or particle.y > world.screen_height + margin
        ):
            particle.is_alive = False