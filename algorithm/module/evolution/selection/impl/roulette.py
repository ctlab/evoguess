from ..selection import *


class Roulette(Selection):
    slug = 'selection:roulette'
    name = 'Roulette(Selection)'

    def breed(self, population: Vector, size: int) -> Vector:
        population = list(population)

        ranges, rng, count = [], 0, len(population)
        for i in range(count):
            w = 0.
            for j in range(count):
                w += population[i].get() / population[j].get()
            rng = rng + (1. / w) if (i != count - 1) else 1.
            ranges.append(rng)

        def get(prob):
            for k in range(1, count):
                if ranges[k] >= prob:
                    return population[k - 1]
            return population[-1]

        return [get(p) for p in self.random_state.rand(size)]


__all__ = [
    'Roulette'
]
