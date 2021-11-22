from .._abc.core import *
from ..static import CACHE
from algorithm.typings import *


class Optimization(Core):
    slug = 'core:optimization'
    name = 'Optimization(Core)'

    def __init__(self, algorithm, sampling, *args, **kwargs):
        self.sampling = sampling
        self.algorithm = algorithm
        super().__init__(*args, **kwargs)

        CACHE.canceled = {}
        CACHE.estimated = {}
        CACHE.estimating = {}

        self.optimization_trace = []

    # def estimate(self, *points: Point, count: int, timeout: float = None) -> Vector:
    #     not_estimated = collection.trim(points, lambda x: not x.estimate)
    #     count = max(0, (count or len(points)) - len(points) + len(not_estimated))
    #
    #     p_handles = [self._queue(p) for p in points if not p.estimated]
    #     estimated, _ = self._await(*p_handles, count=len(p_handles))
    #
    #     return points

    def launch(self, *points: Point):
        # root = self.estimate(*points, timeout=self.limit.left().get('time'))
        pass

    def launch_from_vector(self, vector: Vector):
        return self.launch(*vector)

    def launch_from_backdoors(self, *backdoors):
        return self.launch(*map(Point, backdoors))


__all__ = [
    'Point',
    'Optimization'
]
