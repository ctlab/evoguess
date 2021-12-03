from ..mutation import *

from math import pow


class Doer(Mutation):
    name = 'Mutation: Doer'

    def __init__(self, beta=3, **kwargs):
        super().__init__(**kwargs)
        self.beta = beta

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

    def mutate(self, i: Individual) -> Individual:
        v = i.backdoor.get_mask()
        p = self.__get_alpha(len(v)) / len(v)

        while True:
            distribution = self.random_state.rand(len(v))
            if p > min(distribution):
                break

        for j in range(len(v)):
            if p > distribution[j]:
                v[j] = not v[j]

        return Individual(i.backdoor.get_copy(v))

    def __str__(self):
        return '%s (beta: %d, seed: %s)' % (self.name, self.beta, self.seed)


__all__ = ['Doer']
