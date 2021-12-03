from typing import Iterable
from numpy.random.mtrand import RandomState
from structure.individual import Population


class Selection:
    name = 'Selection'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', 2 ** 32 - 1)
        self.random_state = RandomState(seed=self.seed)

    def breed(self, population: Population, size: int) -> Population:
        raise NotImplementedError

    def configure(self, state):
        pass

    def __str__(self):
        return '%s (seed: %s)' % (self.name, self.seed)


__all__ = [
    'Iterable',
    'Selection',
    'Population'
]
