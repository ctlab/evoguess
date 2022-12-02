from math import sqrt
from typing import Dict, Any

from ..sampling import Sampling
from util.iterable import concat
from function.models import Results


class Epsilon(Sampling):
    slug = 'sampling:epsilon'

    def __init__(self, step: int, min_size: int, max_size: int,
                 epsilon: float, split_into: int, delta: float = 0.05):
        super().__init__(max_size, split_into)
        self.epsilon, self.delta = epsilon, delta
        self.min_size, self.step = min_size, step

    def _get_epsilon(self, results: Results):
        values = concat(*[r.values.values() for r in results])
        size, expected = len(values), sum(values) / len(values)
        deviations = sum([(value - expected) ** 2 for value in values])
        return sqrt(deviations / (size - 1) / (self.delta * size)) / expected

    def summarize(self, results: Results) -> Dict[str, Any]:
        return {
            'epsilon': self._get_epsilon(results)
        }

    def get_count(self, offset: int, size: int, results: Results) -> int:
        if offset == 0:
            return min(self.min_size, size)
        elif offset < size and offset < self.max_size:
            if self._get_epsilon(results) > self.epsilon:
                count = min(offset + self.step, self.max_size, size)
                return max(0, count - offset)
        return 0

    def __config__(self):
        return {
            'slug': self.slug,
            'step': self.step,
            'delta': self.delta,
            'epsilon': self.epsilon,
            'min_size': self.min_size,
            'max_size': self.max_size,
            'split_into': self.split_into
        }


__all__ = [
    'Epsilon'
]
