from ..._abc.iterable.genetic import *

from util.array import slicer


class Elitism(Genetic):
    slug = 'iterable:elitism'
    name = 'Algorithm(Iterable): Elitism'

    def __init__(self, size, elites, *args, **kwargs):
        self.population_size = size - elites
        self.elites, self.size = elites, size
        assert size > elites, "Population size less then count of elites"
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        children = []
        for chunk in slicer(self.tweak_chunk_size, selected):
            if len(chunk) == self.tweak_chunk_size:
                chunk = self.crossover.cross(*chunk)
            mutated = map(self.mutation.mutate, chunk)
            children.extend(mutated)
        return children

    def join(self, parents: Population, children: Population):
        population = sorted(parents)[:self.elites]
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
