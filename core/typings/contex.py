from typing import Optional, NamedTuple

from ..static import CORE_CACHE
from util.collection import pick_by
from function.typings import TaskId, TaskResult, Estimation


class JobTask(NamedTuple):
    id: TaskId
    index: int


class Context:
    def __init__(self, backdoor, instance, **kwargs):
        self.backdoor = backdoor
        self.instance = instance

        self.space = kwargs.get('space')
        self.function = kwargs.get('function')
        self.sampling = kwargs.get('sampling')
        self.executor = kwargs.get('executor')
        self.job_seed = kwargs.get('job_seed')
        self.state = self.sampling.get_state(
            self.job_seed, backdoor.task_count()
        )

    def get_tasks(self, results: list[TaskResult]) -> list[JobTask]:
        tasks, offset = [], len(results)
        count = self.sampling.get_count(self.backdoor, results)

        if count > 0:
            if self.power > self.sampling.max_size:
                value = self.job_seed
                tasks = [JobTask(i, value + i) for i in range(offset, offset + count)]
            else:
                values = self._get_sequence()
                tasks = [JobTask(i, values[i]) for i in range(offset, offset + count)]
        return tasks

    def get_estimation(self, results: list[TaskResult] = None) -> Estimation:
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

    def get_limits(self, results: list[TaskResult]) -> tuple[int, Optional[int]]:
        return 0, None

    def is_reasonably(self, futures, values):
        return True


__all__ = [
    'JobTask',
    'Context',
]
