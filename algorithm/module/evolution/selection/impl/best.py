from ..selection import *


class Best(Selection):
    slug = 'selection:best'
    name = 'Best(Selection)'

    def __init__(self, number_of_bests=1, **kwargs):
        super().__init__(**kwargs)
        self.number_of_bests = number_of_bests

    def breed(self, population: Vector, size: int) -> Vector:
        s_population = sorted(population)
        nob = min(self.number_of_bests, len(population))
        selected = [s_population[i % nob] for i in range(size)]
        self.random_state.shuffle(selected)
        return selected

    def __info__(self):
        return {
            **super().__info__(),
            'number_of_bests': self.number_of_bests
        }


__all__ = [
    'Best'
]
