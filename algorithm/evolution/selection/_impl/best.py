from ..selection import *


class Best(Selection):
    name = 'Selection: Best'

    def __init__(self, number_of_bests=1, **kwargs):
        super().__init__(**kwargs)
        self.number_of_bests = number_of_bests

    def breed(self, population: Population, size: int) -> Population:
        s_population = sorted(population)
        nob = min(self.number_of_bests, len(population))
        selected = [s_population[i % nob] for i in range(size)]
        self.random_state.shuffle(selected)
        return selected

    def __str__(self):
        return '%s (nob: %d, seed: %s)' % (self.name, self.number_of_bests, self.seed)


__all__ = [
    'Best'
]
