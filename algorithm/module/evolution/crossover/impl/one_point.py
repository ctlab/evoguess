from ..crossover import *


class OnePoint(Crossover):
    slug = 'crossover:one-point'
    name = 'One-point(Crossover)'

    def cross(self, ind1: Point, ind2: Point):
        vbd, wbd = ind1.backdoor, ind2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        direction = self.random_state.rand()
        pos = self.random_state.randint(len(v))
        a, b = (0, pos) if direction < 0.5 else (pos, len(v))

        for i in range(a, b):
            v[i], w[i] = w[i], v[i]

        return Point(vbd.get_copy(v)), Point(wbd.get_copy(w))


__all__ = [
    'OnePoint'
]
