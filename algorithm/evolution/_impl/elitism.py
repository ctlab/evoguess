from ..genetic import *
import re


class Elitism(Genetic):
    def __init__(self, size: int, elites: int, *args, **kwargs):
        self.population_size = size - elites
        self.elites, self.size = elites, size
        self.name = 'Algorithm: Elitism (%d over %d)' % (elites, size)
        assert size > elites, "Population size less then count of elites"
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        selected, children = list(selected), []
        for i in range(0, len(selected) - 1, 2):
            i1, i2 = selected[i], selected[i + 1]
            crossed = self.crossover.cross(i1, i2)
            mutated = map(self.mutation.mutate, crossed)
            children.extend(mutated)

        if len(selected) > len(children):
            children.append(self.mutation.mutate(selected[-1]))

        return children

    def join(self, parents: Population, children: Population):
        elites = sorted(parents)[:self.elites]
        mobs = sorted(children)[:self.size - self.elites]
        return elites + mobs

    @staticmethod
    def parse(params):
        args = re.findall(r'(\d+)\^(\d+)', params)
        return {
            'size': int(args[0][1]),
            'elites': int(args[0][0])
        } if len(args) else None


__all__ = [
    'Elitism'
]
