from typing import Optional

from ..static import CORE_CACHE
from util.collection import pick_by
from function.typings import Estimation, Results, WorkerArgs


class Context:
    def __init__(self, backdoor, instance, **kwargs):
        self.backdoor = backdoor
        self.instance = instance

        self.space = kwargs.get('space')
        self.shaping = kwargs.get('shaping')
        self.function = kwargs.get('function')
        self.sampling = kwargs.get('sampling')
        self.executor = kwargs.get('executor')
        self.job_seed = kwargs.get('job_seed')

        self.sample_size = min(backdoor.task_count(), self.sampling.max_size) \
            if not self.function.supbs_required else self.sampling.max_size
        self.sample_state = self.sampling.get_state(0, self.sample_size)

    def get_tasks(self, results: Results) -> list[WorkerArgs]:
        # todo: pass shape model to sample_state
        return [
            (self.job_seed, self.sample_size, offset, length) for offset, length
            in self.sample_state.chunks(self.executor.workers, results)
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
