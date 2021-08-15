from .evolution import *


class Genetic(Evolution):
    tweak_chunk_size = 2
    name = 'Algorithm(Iterable): Genetic'

    def __init__(self, crossover, *args, **kwargs):
        self.crossover = crossover
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    def __info__(self):
        return {
            **super().__info__(),
            'crossover': self.crossover.__info__()
        }


__all__ = [
    'Genetic',
    'Population',
]
