from ..sampling import *

from math import sqrt


class Epsilon(Sampling):
    slug = 'sampling:epsilon'
    name = 'Sampling: Epsilon'

    def __init__(self, order, mn, mx, step, eps, delta=0.05):
        super().__init__(order, mx, step)
        self.eps, self.delta = eps, delta
        self.min, self.max, self.step = mn, mx, step

    def _n_e_d(self, values):
        n = len(values)
        e = sum(values) / n
        d = sum([(value - e) ** 2 for value in values]) / (n - 1)
        return n, e, d

    def _get_eps(self, values):
        n, e, d = self._n_e_d(values)
        return sqrt(d / (self.delta * n)) / e

    def get_count(self, backdoor, values=()):
        # todo: filter None values
        count = len(values)
        bd_count = backdoor.task_count()
        if count == 0:
            return min(self.min, bd_count)
        elif count < bd_count and count < self.max:
            if self._get_eps(values) > self.eps:
                bound = min(count + self.step, self.max, bd_count)
                return bound - count
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
            'epsilon': self.eps,
        }


__all__ = [
    'Epsilon'
]
