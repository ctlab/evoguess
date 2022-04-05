from enum import Enum

from function.typings import TaskResult


class SamplingOrder(Enum):
    RANDOM = 0
    DIRECT = 1
    REVERSED = 2


class Sampling:
    slug = 'sampling'
    name = 'Sampling'

    def __init__(self, max_size: int, order: SamplingOrder = SamplingOrder.RANDOM, *args, **kwargs):
        self.order = order
        self.max_size = max_size

        self.

    def _get_sequence(self):
        if self.sequence is None:
            if self.sampling.order == self.sampling.RANDOM:
                rs = RandomState(seed=self.job_seed)
                self.sequence = rs.permutation(self.power)
            elif self.sampling.order == self.sampling.DIRECT:
                self.sequence = list(range(self.power))
            elif self.sampling.order == self.sampling.REVERSED:
                self.sequence = list(range(self.power))[::-1]
        return self.sequence

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
