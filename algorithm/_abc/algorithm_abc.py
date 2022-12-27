from .algorithm import *

from time import time as now
from method.typings.handle import n_completed


class AlgorithmABC(Algorithm):
    name = 'Algorithm(ABC)'

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.root, self.best = None, None

    def preprocess(self, *points: Point) -> Vector:
        index_value = self.limit.set('index', 0)
        self.root = [p for p in points if p.estimated]
        p_handles = [self._queue(p) for p in points if not p.estimated]
        estimated, _ = self._await(*p_handles, count=len(p_handles))
        self.root.extend(estimated)

        self._proceed_index_result(index_value, self.root)
        self.best = min(self.root)
        return self.root

    def process(self, estimated: Vector) -> Vector:
        raise NotImplementedError

    def _await(self, *point_handles, count):
        count = min(count, len(point_handles))
        timeout = self.limit.left().get('time')
        handles = [h for (_, h) in point_handles]
        done = n_completed(handles, count, timeout)
        self.limit.set('time', now() - self.start_stamp)

        estimated, left_point_handles = [], []
        for point, handle in point_handles:
            if handle not in done:
                left_point_handles.append((point, handle))
            else:
                estimated.append(point.set(**handle.result()))

        return estimated, left_point_handles

    # noinspection PyMethodMayBeStatic
    def _cancel(self, point_handle):
        point, handle = point_handle
        return point.set(**handle.cancel_and_result())

    def _update_best(self, *points):
        if len(points) > 0:
            prev_best = self.best
            self.best = min(self.best, *points)
            if self.best != prev_best:
                self.limit.set('stagnation', 0)
            else:
                self.limit.increase('stagnation')


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'AlgorithmABC',
]
