from .mu_comma_lambda import *


class MuPlusLambda(MuCommaLambda):
    slug = 'iterable:plus'
    name = 'Algorithm(Iterable): Evolution (μ + λ)'

    def join(self, parents: Population, children: Population):
        mu_parents = sorted(parents)[:self.mu]
        lmbda_children = sorted(children)[:self.lmbda]
        return mu_parents + lmbda_children


__all__ = [
    'MuPlusLambda'
]
