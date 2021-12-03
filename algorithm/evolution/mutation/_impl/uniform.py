from ..mutation import *


class Uniform(Mutation):
    name = 'Mutation: Uniform'

    def __init__(self, scale=1., **kwargs):
        super().__init__(**kwargs)
        self.scale = scale

    def mutate(self, i: Individual) -> Individual:
        v = i.backdoor.get_mask()
        p = self.scale / len(v)

        while True:
            distribution = self.random_state.rand(len(v))
            if p > min(distribution):
                break

        for j in range(len(v)):
            if p > distribution[j]:
                v[j] = not v[j]

        return Individual(i.backdoor.get_copy(v))

    def __str__(self):
        return '%s (scale: %.2f, seed: %d)' % (self.name, self.scale, self.seed)


__all__ = ['Uniform']
