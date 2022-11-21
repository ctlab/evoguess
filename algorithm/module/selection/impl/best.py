from ..selection import *

from typings.optional import Int
from core.model.point import Vector


class Best(Selection):
    slug = 'selection:best'

    def __init__(self, best_count: int, random_seed: Int = None):
        self.best_count = best_count
        super().__init__(random_seed)

    def breed(self, vector: Vector, size: int) -> Vector:
        mx = min(self.best_count, len(vector))
        return [
            sorted(vector)[i % mx] for i in
            self.random_state.permutation(size)
        ]

    def __info__(self):
        return {
            **super().__info__(),
            'best_count': self.best_count
        }


__all__ = [
    'Best'
]
