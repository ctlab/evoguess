from ..sampling import *

from math import sqrt


class Epsilon(Sampling):
    slug = 'sampling:epsilon'

    def __init__(self,
                 step: int, epsilon: float,
                 min_count: int, max_count: int,
                 delta: float = 0.05, **kwargs):
        self.step = step
        self.delta = delta
        self.epsilon = epsilon
        self.min, self.max = min_count, max_count
        super().__init__(self.max, **kwargs)

    def _n_e_d(self, values):
        n, e = len(values), sum(values) / len(values)
        return n, e, sum([(value - e) ** 2 for value in values]) / (n - 1)

    def _get_eps(self, results: Results):
        # todo: count eps using results instead values
        n, e, d = self._n_e_d(values)
        return sqrt(d / (self.delta * n)) / e

    def summarize(self, results: Results) -> Dict[str, Any]:
        return {
            'epsilon': self._get_eps(results)
        }

    def get_count(self, offset: int, size: int, results: Results) -> int:
        if offset == 0:
            return min(self.min, size)
        elif offset < size and offset < self.max:
            if self._get_eps(results) > self.epsilon:
                count = min(offset + self.step, self.max, size)
                return max(0, count - offset)
        return 0

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
