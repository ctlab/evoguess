from numpy.random.mtrand import RandomState
from structure.individual import Individual


class Mutation:
    name = 'Mutation'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', 2 ** 32 - 1)
        self.random_state = RandomState(seed=self.seed)

    def mutate(self, i: Individual) -> Individual:
        raise NotImplementedError

    def configure(self, limits):
        pass

    def __str__(self):
        return '%s (seed: %s)' % (self.name, self.seed)


__all__ = [
    'Mutation',
    'Individual'
]
