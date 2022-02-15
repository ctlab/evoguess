from ..._abc._async.evolution import *


class MuPlusLambda(Evolution):
    slug = 'evolution:plus'
    name = 'Algorithm: Evolution (μ + λ)'

    def __init__(self, mu, lmbda, *args, **kwargs):
        self.population_size = lmbda
        self.mu, self.lmbda = mu, lmbda
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        return list(map(self.mutation.mutate, selected))

    def join(self, parents: Population, children: Population):
        return sorted([*parents, *children])[:self.mu]

    def __info__(self):
        return {
            **super().__info__(),
            'mu': self.mu,
            'lmbda': self.lmbda
        }


__all__ = [
    'MuPlusLambda'
]
