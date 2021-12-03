from ..selection import *


class Roulette(Selection):
    name = 'Selection: Roulette'

    def breed(self, population: Population, size: int) -> Population:
        population = list(population)

        ranges, rng, count = [], 0, len(population)
        for i in range(count):
            w = 0.
            for j in range(count):
                w += population[i].value / population[j].value
            rng = rng + (1. / w) if (i != count - 1) else 1.
            ranges.append(rng)

        def get(prob):
            for k in range(1, count):
                if ranges[k] >= prob:
                    return population[k - 1]

        return [get(p) for p in self.random_state.rand(size)]


__all__ = [
    'Roulette'
]
