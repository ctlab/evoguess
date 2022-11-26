from ..selection import *

from core.model.point import Vector


class Roulette(Selection):
    slug = 'selection:roulette'

    def select(self, vector: Vector, size: int) -> Vector:
        ranges, rng, count = [], 0, len(vector)
        for i, point1 in enumerate(vector):
            w = 0.
            for point2 in vector:
                w += point1.value() / point2.value()
            rng = rng + (1. / w) if (i != count - 1) else 1.
            ranges.append(rng)

        def get(prob):
            for k in range(1, count):
                if ranges[k] >= prob:
                    return vector[k - 1]
            return vector[-1]

        return [get(p) for p in self.random_state.rand(size)]


__all__ = [
    'Roulette'
]
