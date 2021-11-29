from ..sampling import *

from math import sqrt
from util.collection import trim


class Epsilon(Sampling):
    slug = 'sampling:epsilon'
    name = 'Sampling: Epsilon'

    def __init__(self, step, epsilon, delta=0.05, *args, **kwargs):
        self.step = step
        self.delta = delta
        self.epsilon = epsilon
        self.min, self.max = kwargs['min'], kwargs['max']
        super().__init__(self.max, *args, **kwargs)

    def _n_e_d(self, values):
        n = len(values)
        e = sum(values) / n
        d = sum([(value - e) ** 2 for value in values]) / (n - 1)
        return n, e, sum([(value - e) ** 2 for value in values]) / (n - 1)

    def _get_eps(self, values):
        n, e, d = self._n_e_d(values)
        return sqrt(d / (self.delta * n)) / e

    def get_count(self, backdoor, values):
        count = len(values)
        bd_count = backdoor.task_count()

        if count == 0:
            return min(self.min, bd_count)
        elif count < bd_count and count < self.max:
            if self._get_eps(trim(values)) > self.epsilon:
                bound = min(count + self.step, self.max, bd_count)
                return max(0, bound - count)
        return 0

    def get_size(self):
        return self.max, self.step

    def report(self, values):
        return {
            'epsilon': self._get_eps(values)
        }

    def __info__(self):
        return {
            **super().__info__(),
            'min': self.min,
            'max': self.max,
            'step': self.step,
            'delta': self.delta,
            'epsilon': self.epsilon,
        }


__all__ = [
    'Epsilon'
]
