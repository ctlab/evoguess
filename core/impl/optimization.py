from .._abc import Estimator
from ..static import CACHE

from ..typings.handle import n_completed

from time import time as now
from util.operator import smin


class Optimization(Estimator):
    slug = 'core:optimization'
    name = 'Optimization(Core)'

    def __init__(self, algorithm, sampling, space, *args, **kwargs):
        self.space = space
        self.sampling = sampling
        self.algorithm = algorithm
        super().__init__(*args, **kwargs)

        CACHE.best = None
        self.optimization_trace = []

    def launch(self):
        self.start_stamp = now()
        # todo: provide cache
        handles = []
        awaited = self.algorithm.awaited_count
        backdoor = self.space.get(self.instance)
        point = self._await(self.estimate(backdoor))
        with self.algorithm.start(point) as algorithm:
            while not self.limitation.exhausted():
                backdoors = algorithm.get_backdoors()
                handles.extend(map(self.estimate, backdoors))
                estimated, handles = self._await(handles, awaited)
                algorithm.update_vector(estimated)

                spent_time = now() - self.start_stamp
                self.limitation.set('time', spent_time)
                # self.limitation.update(algorithm)

            solution = algorithm.solution()

        return solution

    def _await(self, *handles, count=None):
        timeout = self.limitation.left()
        count = smin(count, len(handles))
        done = n_completed(handles, count, timeout)

        estimated, left_handles = [], []
        for handle in handles:
            if handle not in done:
                left_handles.append(handle)
            else:
                estimated.append(handle.result())

        return estimated, left_handles


__all__ = [
    'Optimization'
]
