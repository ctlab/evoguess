from ..._abc._async.evolution import *

from numpy import argsort
from util.collection import pick_by, omit_by


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
        mu_indexes = argsort(parents)[:self.mu]
        filler_size = max(0, self.lmbda - len(children))
        lmbda_filler = omit_by(parents, mu_indexes)[:filler_size]
        return [*pick_by(parents, mu_indexes), *children, *lmbda_filler]

    def __info__(self):
        return {
            **super().__info__(),
            'mu': self.mu,
            'lmbda': self.lmbda
        }


__all__ = [
    'MuPlusLambda'
]
