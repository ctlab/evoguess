from ..crossover import *

from typing import Tuple
from core.model.point import Point


class OnePoint(Crossover):
    slug = 'crossover:one-point'

    def cross(self, p1: Point, p2: Point) -> Tuple[Point, Point]:
        bd1, bd2 = p1.backdoor, p2.backdoor
        mask1, mask2 = bd1.get_mask(), bd2.get_mask()

        a = self.random_state.randint(len(mask1))
        b = self.random_state.randint(2) * len(mask1)
        for i in range(min(a, b), max(a, b)):
            mask1[i], mask2[i] = mask2[i], mask1[i]

        return p1.new(bd1.get_copy(mask1)), p2.new(bd2.get_copy(mask2))


__all__ = [
    'OnePoint'
]
