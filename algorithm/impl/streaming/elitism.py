from ..._abc.streaming.genetic import *

from util.array import chunk_slice


class Elitism(Genetic):
    slug = 'streaming:elitism'
    name = 'Algorithm(Streaming): Elitism'

    def __init__(self, size, elites, *args, **kwargs):
        self.population_size = size - elites
        self.elites, self.size = elites, size
        assert size > elites, "Population size less then count of elites"
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        children = []
        for chunk in chunk_slice(self.min_tweak_size, selected):
            if len(chunk) == self.min_tweak_size:
                chunk = self.crossover.cross(*chunk)
            mutated = map(self.mutation.mutate, chunk)
            children.extend(mutated)
        return children

    def join(self, parents: Population, children: Population):
        population = sorted(parents)[:self.size - len(children)]
        return population + list(children)

    def __info__(self):
        return {
            **super().__info__(),
            'size': self.size,
            'elites': self.elites,
        }


__all__ = [
    'Elitism'
]
