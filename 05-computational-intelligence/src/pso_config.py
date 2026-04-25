import random


def _objective(pos: list, benign_fn) -> float:
    """
    Penalise configs that either break benign scripts
    or grant too many resources (large limits = high cost).
    pos = [memory_mb, cpu_fraction, timeout_s]
    benign_fn(pos) -> bool (True = benign script still completes)
    """
    memory_mb, cpu_frac, timeout_s = pos
    if not benign_fn(pos):
        return 1e6             # hard penalty — benign script broke
    return memory_mb / 512 + cpu_frac + timeout_s / 60   # minimise resources


def pso_config_search(benign_fn, n_particles: int = 15,
                      iterations: int = 40) -> list:
    """
    Find minimal safe sandbox resource limits using PSO.
    Returns [memory_mb, cpu_fraction, timeout_s].
    """
    bounds = [(64, 512), (0.1, 1.0), (5, 60)]

    positions  = [[random.uniform(lo, hi) for lo, hi in bounds]
                  for _ in range(n_particles)]
    velocities = [[0.0] * 3 for _ in range(n_particles)]
    pbest      = [p[:] for p in positions]
    gbest      = min(pbest, key=lambda p: _objective(p, benign_fn))

    for _ in range(iterations):
        for i, (pos, vel) in enumerate(zip(positions, velocities)):
            new_vel, new_pos = [], []
            for j in range(3):
                lo, hi = bounds[j]
                v = (0.7 * vel[j]
                     + 1.5 * random.random() * (pbest[i][j] - pos[j])
                     + 1.5 * random.random() * (gbest[j] - pos[j]))
                p = max(lo, min(hi, pos[j] + v))
                new_vel.append(v)
                new_pos.append(p)
            positions[i], velocities[i] = new_pos, new_vel
            if _objective(new_pos, benign_fn) < _objective(pbest[i], benign_fn):
                pbest[i] = new_pos[:]
        gbest = min(pbest, key=lambda p: _objective(p, benign_fn))

    return [round(x, 3) for x in gbest]