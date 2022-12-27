from ..mutation import *
from math import pow


class Doer(Mutation):
    slug = 'mutation:doer'
    name = 'Doer(Mutation)'

    def __init__(self, beta=3, **kwargs):
        self.beta = beta
        super().__init__(**kwargs)

    def __get_alpha(self, size):
        bound = size // 2 + 1
        if bound < 3:
            return 1

        ll, p, rr = 0., self.random_state.rand(), 0.
        c = sum(1. / pow(i, self.beta) for i in range(1, bound))
        for k in range(1, bound):
            ll = rr
            rr += (1. / (c * pow(k, self.beta)))
            if ll <= p < rr:
                return k

        return bound - 1

    def mutate(self, i: Point) -> Point:
        v = i.backdoor.get_mask()
        p = self.__get_alpha(len(v)) / len(v)
        distribution = self.roll_distribution(p, len(v))

        for j in range(len(v)):
            if p > distribution[j]:
                v[j] = not v[j]

        return Point(i.backdoor.get_copy(v))

    def __info__(self):
        return {
            **super().__info__(),
            'beta': self.beta
        }


__all__ = [
    'Doer'
]
