from ..._abc.streaming.evolution import *


class MuPlusLambda(Evolution):
    slug = 'streaming:plus'
    name = 'Algorithm(Streaming): Evolution (μ + λ)'

    def __init__(self, mu, lmbda, *args, **kwargs):
        self.population_size = lmbda
        self.mu, self.lmbda = mu, lmbda
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        return list(map(self.mutation.mutate, selected))

    def join(self, parents: Population, children: Population):
        population = sorted(parents)[:self.mu + self.lmbda - len(children)]
        return population + list(children)

    def __info__(self):
        return {
            **super().__info__(),
            'mu': self.mu,
            'lmbda': self.lmbda
        }


__all__ = [
    'MuPlusLambda'
]
