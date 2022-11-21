from executor import Executor
from function import Function
from instance import Instance
from algorithm import Algorithm

from time import time as now
from typing import Tuple, List

from ..abc import Estimate
from ..static import CORE_CACHE
from ..model.point import Vector
from ..model.handle import Handle, n_completed

from ..module.space import Space
from ..module.sampling import Sampling
from ..module.comparator import Comparator
from ..module.limitation import Limitation

from output import Logger
from typings.optional import Int
from util.iterable import omit_by

Await = Tuple[Vector, List[Handle]]


class Optimize(Estimate):
    slug = 'core:optimization'

    def __init__(self,
                 space: Space,
                 logger: Logger,
                 executor: Executor,
                 instance: Instance,
                 sampling: Sampling,
                 function: Function,
                 algorithm: Algorithm,
                 comparator: Comparator,
                 limitation: Limitation,
                 random_seed: Int = None):
        self.algorithm = algorithm
        self.limitation = limitation
        super().__init__(space, logger, instance, executor,
                         sampling, function, comparator, random_seed)

        self.start_stamp = None
        self.optimization_trace = []
        CORE_CACHE.best_point = None

    def launch(self, *args, **kwargs) -> Vector:
        with self.logger:
            self.start_stamp = now()
            # self.logger.config(self.__config__())
            # todo: search root estimation in cache
            initial = self.space.get_initial(self.instance)
            point, handles = self.estimate(initial).result(), []
            assert point.estimated(), 'initial isn\'t estimated!'
            self._log_insertion((0, [point]), now() - self.start_stamp)
            with self.algorithm.start(point) as point_manager:
                while not self.limitation.exhausted():
                    handles.extend([
                        self.estimate(backdoor) for backdoor in
                        point_manager.collect(len(handles), 1)
                    ])
                    estimated, handles = self._await(*handles)
                    insertion = point_manager.insert(*estimated)

                    spent_time = now() - self.start_stamp
                    self.limitation.set('time', spent_time)
                    self._log_insertion(insertion, spent_time)

                [h.cancel() for h in handles]
                return point_manager.solution()

    def _await(self, *handles: Handle, count: int = 1) -> Await:
        count = count or len(handles)
        timeout = self.limitation.left('time')
        done = n_completed(handles, count, timeout)
        not_done = omit_by(handles, lambda h: h in done)
        return [h.result() for h in done], not_done

    def _log_insertion(self, insertion: Tuple[int, Vector], spent: float):
        if insertion is not None:
            index, vector = insertion
            self.logger.write(vector, index=index, spent=spent)

    def __config__(self):
        return {}


__all__ = [
    'Optimize'
]
