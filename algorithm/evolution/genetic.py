from .evolution import *
from .crossover.crossover import Crossover


class Genetic(Evolution):
    name = 'Algorithm: Genetic'

    def __init__(self,
                 crossover: Crossover,
                 *args, **kwargs
                 ):
        self.crossover = crossover
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    @staticmethod
    def parse(params):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            self.selection,
            self.mutation,
            self.crossover,
            '--------------------',
            self.method,
        ]))


__all__ = [
    'Genetic',
    'Population',
]
