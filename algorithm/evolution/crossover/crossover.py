from typing import Tuple
from numpy.random.mtrand import RandomState
from structure.individual import Individual


class Crossover:
    name = 'Crossover'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', 2 ** 32 - 1)
        self.random_state = RandomState(seed=self.seed)

    def cross(self, i1: Individual, i2: Individual) -> Tuple[Individual, Individual]:
        raise NotImplementedError

    def configure(self, state):
        pass

    def __str__(self):
        return '%s (seed: %s)' % (self.name, self.seed)


__all__ = [
    'Tuple',
    'Crossover',
    'Individual'
]
