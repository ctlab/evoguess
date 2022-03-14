from .._abc.genetic import *

from numpy import argsort
from util.array import slice_by_size
from util.collection import get_by_indexes, trim_by_indexes


class Elitism(Genetic):
    tweak_size = 2
    slug = 'genetic:elitism'
    name = 'Algorithm: Elitism'

    def __init__(self, size, elites, *args, **kwargs):
        self.population_size = size - elites
        self.elites, self.size = elites, size
        assert size > elites, "Population size less then count of elites"
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        children = []
        for chunk in slice_by_size(self.tweak_size, selected):
            if len(chunk) == self.tweak_size:
                chunk = self.crossover.cross(*chunk)
            mutated = map(self.mutation.mutate, chunk)
            children.extend(mutated)
        return children

    def join(self, parents: Population, children: Population):
        elite_indexes = argsort(parents)[:self.elites]
        filler_size = max(0, self.population_size - len(children))
        elite_filler = trim_by_indexes(parents, elite_indexes)[:filler_size]
        return [*get_by_indexes(parents, elite_indexes), *children, *elite_filler]

    def __info__(self):
        return {
            **super().__info__(),
            'size': self.size,
            'elites': self.elites,
        }


__all__ = [
    'Elitism'
]
