from ..crossover import *


class Uniform(Crossover):
    slug = 'crossover:uniform'
    name = 'Uniform(Crossover)'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prob = kwargs.get('prob', 0.2)

    def cross(self, ind1: Point, ind2: Point):
        vbd, wbd = ind1.backdoor, ind2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        distribution = self.random_state.rand(len(v))
        for i in range(len(v)):
            if self.prob >= distribution[i]:
                v[i], w[i] = w[i], v[i]

        return Point(vbd.get_copy(v)), Point(wbd.get_copy(w))

    def __info__(self):
        return {
            **super().__info__(),
            'prob': self.prob
        }


__all__ = [
    'Uniform'
]
