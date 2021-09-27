from ..algorithm_async import *
from util.operator import smin, smax, sget

Individual = Point
Population = Vector


class Evolution(AlgorithmAsync):
    min_await_count = 1
    population_size = None
    name = 'Algorithm(Async): Evolution'

    def __init__(self, mutation, selection, *args, **kwargs):
        self.mutation = mutation
        self.selection = selection
        super().__init__(*args, **kwargs)

        self.await_count = smax(smin(
            self.population_size,
            sget(kwargs, 'await_count')
        ), self.min_await_count)
        self.max_points = self.population_size

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    def get_points(self, vector: Vector, count: int) -> Vector:
        size = count + count % self.min_await_count
        selected = self.selection.breed(vector, size)
        return self.tweak(selected)

    def update_vector(self, vector: Vector, *points: Point) -> Vector:
        return self.join(vector, points)

    def __info__(self):
        return {
            **super().__info__(),
            'mutation': self.mutation.__info__(),
            'selection': self.selection.__info__()
        }


__all__ = [
    'Evolution',
    'Individual',
    'Population',
]
