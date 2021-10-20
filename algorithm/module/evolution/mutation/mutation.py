from algorithm.typings import Point
from numpy.random import randint, RandomState


class Mutation:
    slug = 'mutation'
    name = 'Mutation'

    def __init__(self, **kwargs):
        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.seed)

    def roll_distribution(self, p, length):
        while True:
            distribution = self.random_state.rand(length)
            if p <= 0 or p > min(distribution):
                return distribution

    def mutate(self, ind: Point) -> Point:
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
    'Mutation',
]
