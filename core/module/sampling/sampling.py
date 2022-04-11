from enum import Enum
from typing import NamedTuple

from numpy.random import RandomState


# todo: is it needed at all?
# class SamplingOrder(Enum):
#     [
#         RANDOM,
#         DIRECT,
#         REVERSED
#     ] = range(3)


class SamplingState(NamedTuple):
    seed: int
    power: int
    sequence: list[int]


class Sampling:
    slug = 'sampling'
    name = 'Sampling'

    def __init__(self, max_size: int, *args, **kwargs):
        # self.order = order
        self.regions = 1024
        self.max_size = max_size
        # todo: regions settings

    def get_state(self, seed: int, power: int) -> SamplingState:
        random_state = RandomState(seed=seed)
        if power > self.max_size:
            sequence = random_state.randint(0, self.regions, self.max_size)
        else:
            sequence = random_state.permutation(power)
        return SamplingState(seed, power, list(sequence))

    def generate(self, power: int, values: list[float]):
        raise NotImplementedError

    def summarize(self, values: list[float]):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'order': self.order
        }

    def __str__(self):
        return self.name


__all__ = [
    'Sampling',
    'SamplingOrder'
]
