from ..crossover import *

from typing import Tuple
from typings.optional import Int
from core.model.point import Point


class Uniform(Crossover):
    slug = 'crossover:uniform'

    def __init__(self, swap_prob: float = 0.5, random_seed: Int = None):
        self.swap_prob = swap_prob
        super().__init__(random_seed)

    def cross(self, p1: Point, p2: Point) -> Tuple[Point, Point]:
        bd1, bd2 = p1.backdoor, p2.backdoor
        mask1, mask2 = bd1.get_mask(), bd2.get_mask()

        # todo: use _distribution from tool funcs
        distribution = self.random_state.rand(len(mask1))
        for i, value in enumerate(distribution):
            if self.swap_prob >= value:
                mask1[i], mask2[i] = mask2[i], mask1[i]

        return p1.new(bd1.get_copy(mask1)), p2.new(bd2.get_copy(mask2))

    def __info__(self):
        return {
            **super().__info__(),
            'swap_prob': self.swap_prob
        }


__all__ = [
    'Uniform'
]
