from algorithm.typings import Vector

from numpy.random import randint, RandomState


class Selection:
    slug = None
    name = 'Selection'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.seed)

    def breed(self, population: Vector, size: int):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'seed': self.seed
        }


__all__ = [
    'Vector',
    'Selection',
]
