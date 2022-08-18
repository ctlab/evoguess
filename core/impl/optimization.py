from .._abc import Estimator
from ..model.handle import *
from ..static import CORE_CACHE
from instance.module.variables import Backdoor

from time import time as now
from util.iterable import omit_by


class Optimization(Estimator):
    slug = 'core:optimization'
    name = 'Optimization(Core)'

    def __init__(self, algorithm, sampling, *args, **kwargs):
        self.sampling = sampling
        self.algorithm = algorithm
        super().__init__(*args, **kwargs)

        self.start_stamp = None
        self.optimization_trace = []
        CORE_CACHE.best_point = None

    def launch(self, root: Backdoor, *args, **kwargs) -> Solution:
        self.start_stamp = now()

        awaited = self.algorithm.awaited_count
        # todo: search root estimation in cache
        point, handles = self.estimate(root).result(), []
        assert point.estimated(), 'Root backdoor not estimated'
        with self.algorithm.start(point) as algorithm:
            while not self.limitation.exhausted():
                if len(handles) > algorithm.max_points:
                    count = algorithm.max_points - len(handles)
                    backdoors = algorithm.get_next(count)
                    handles.extend(map(self.estimate, backdoors))

                estimated, handles = self._await(handles, awaited)
                algorithm.update_vector(estimated)

                spent_time = now() - self.start_stamp
                self.limitation.set('time', spent_time)
                # self.limitation.update(algorithm)

            [h.cancel() for h in handles]
            return algorithm.solution()

    def _await(self, *handles: Handle, count: int = None):
        count = count or len(handles)
        timeout = self.limitation.left()
        done = n_completed(handles, count, timeout)
        not_done = omit_by(handles, lambda h: h in done)
        return [h.result() for h in done], not_done


__all__ = [
    'Optimization'
]
