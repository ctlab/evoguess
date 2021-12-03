from ..crossover import *


class Uniform(Crossover):
    name = 'Crossover: Uniform'

    def __init__(self, prob, **kwargs):
        super().__init__(**kwargs)
        self.prob = prob

    def cross(self, i1: Individual, i2: Individual) -> Tuple[Individual, Individual]:
        vbd, wbd = i1.backdoor, i2.backdoor
        v, w = vbd.get_mask(), wbd.get_mask()

        distribution = self.random_state.rand(len(v))
        for i in range(len(v)):
            if self.prob >= distribution[i]:
                v[i], w[i] = w[i], v[i]

        return Individual(vbd.get_copy(v)), Individual(wbd.get_copy(w))

    def __str__(self):
        return '%s (p: %.2f, seed: %s)' % (self.name, self.prob, self.seed)


__all__ = [
    'Uniform'
]
