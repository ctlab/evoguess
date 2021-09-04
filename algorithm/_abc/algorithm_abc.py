from .algorithm import *

from time import time as now
from method.typings.handle import n_completed


class AlgorithmABC(Algorithm):
    name = 'Algorithm ABC'

    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.root, self.best = None, None

    def preprocess(self, *points: Point) -> Vector:
        index_value = self.limit.set('index', 0)
        self.root = [p for p in points if p.estimated]
        p_handles = [self._queue(p) for p in points if not p.estimated]
        estimated, _ = self._await(p_handles, len(p_handles))
        self.root.extend(estimated)

        self._proceed_index_result(index_value, self.root)
        self.best = sorted(self.root)[0]
        return self.root

    def process(self, estimated: Vector) -> Vector:
        raise NotImplementedError

    def _await(self, point_handles, count):
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

    def _cancel(self, point_handles):
        return [
            point.set(**handle.cancel_and_result())
            for point, handle in point_handles
        ]


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'AlgorithmABC',
]
