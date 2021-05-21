from ..crossover import *


class TwoPoint(Crossover):
    slug = 'crossover:two-point'
    name = 'Two-point(Crossover)'

    def cross(self, ind1: Point, ind2: Point):
        vbd, wbd = ind1.backdoor, ind2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        a = self.random_state.randint(len(v))
        b = self.random_state.randint(len(v))
        a, b = min(a, b), max(a, b)

        for i in range(a, b):
            v[i], w[i] = w[i], v[i]

        return Point(vbd.get_copy(v)), Point(wbd.get_copy(w))


__all__ = [
    'TwoPoint'
]
