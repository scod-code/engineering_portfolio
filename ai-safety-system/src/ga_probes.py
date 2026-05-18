import random


def _make_probe():
    """Chromosome: [timeout_ratio, network_flag, input_noise_level]"""
    return [random.random(), float(random.randint(0, 1)), random.random()]


def evolve_probes(harness_fn, n_probes: int = 20, n_gen: int = 30,
                  mutation_rate: float = 0.2):
    """
    Evolve sandbox probes to maximise risk score.
    harness_fn(probe) -> float (risk score)
    Returns (best_score, best_probe).
    """
    population = [_make_probe() for _ in range(n_probes)]

    for gen in range(n_gen):
        scored = sorted([(harness_fn(p), p) for p in population],
                        reverse=True, key=lambda x: x[0])
        parents = [p for _, p in scored[:n_probes // 2]]

        offspring = []
        while len(offspring) < n_probes:
            a, b  = random.sample(parents, 2)
            cut   = random.randint(1, len(a) - 1)
            child = a[:cut] + b[cut:]
            child = [g + random.gauss(0, 0.1) if random.random() < mutation_rate
                     else g for g in child]
            offspring.append(child)
        population = offspring

    scored = sorted([(harness_fn(p), p) for p in population],
                    reverse=True, key=lambda x: x[0])
    return scored[0]  # (best_score, best_probe)


def random_probe_baseline(harness_fn, n_probes: int = 20):
    """Random baseline — compare GA against this."""
    scores = [harness_fn(_make_probe()) for _ in range(n_probes)]
    return sum(scores) / len(scores), max(scores)
