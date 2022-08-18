from executor import Executor
from instance import Instance
from function import Function

from ..static import CORE_CACHE
from ..module.sampling import Sampling

from typings.optional import Int
from instance.module.variables import Backdoor
from function.typings import Estimation, Results, WorkerArgs

from typing import List
from util.iterable import pick_by


class Context:
    def __init__(self,
                 job_seed: Int,
                 backdoor: Backdoor,
                 instance: Instance,
                 function: Function,
                 sampling: Sampling,
                 executor: Executor):
        self.job_seed = job_seed
        self.backdoor = backdoor
        self.instance = instance
        self.function = function
        self.sampling = sampling
        self.executor = executor

        # todo: change function.supbs_required to instance.input_overflow
        self.sample_size = min(backdoor.power(), self.sampling.max_size) \
            if not self.function.supbs_required else self.sampling.max_size
        self.sample_state = self.sampling.get_state(0, self.sample_size)

    def get_tasks(self, results: Results) -> List[WorkerArgs]:
        return [
            (self.job_seed, self.sample_size, offset, length)
            for offset, length in self.sample_state.chunks(results)
        ]

    def get_estimation(self, results: Results = None) -> Estimation:
        del CORE_CACHE.estimating[self.backdoor]
        if results is None:
            CORE_CACHE.canceled[self.backdoor] = self.job_seed
            return {'job_seed': self.job_seed, 'canceled': True}

        picked = pick_by(results)
        estimation = CORE_CACHE.estimated[self.backdoor] = {
            'job_seed': self.job_seed,
            'accuracy': len(picked) / len(results),
            **self.sampling.summarize(picked),
            **self.function.calculate(self.backdoor, picked),
        }
        return estimation

    # def get_limits(self, results: Results) -> tuple[int, Optional[int]]:
    #     return 0, None
    #
    # def is_reasonably(self, futures, results: Results):
    #     return True


__all__ = [
    'Context',
]
