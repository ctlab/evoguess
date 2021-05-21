from typing import Tuple
from algorithm._type import Point

from numpy.random import randint, RandomState


class Crossover:
    slug = None
    name = 'Crossover'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.seed)

    def cross(self, ind1: Point, ind2: Point):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'seed': self.seed
        }

    def __str__(self):
        return self.name


__all__ = [
    'Point',
    'Tuple',
    'Crossover',
]
