from .._abc.core import *
from ..static import CACHE

from ..typings.job import Job
from ..typings.contex import Context
from ..typings.handle import VoidHandle, JobHandle


class Estimator(Core):
    def __init__(self, sampling, function, *args, **kwargs):
        self.sampling = sampling
        self.function = function
        super().__init__(*args, **kwargs)

    def launch(self, *args, **kwargs):
        raise NotImplementedError

    def estimate(self, backdoor):
        if backdoor in CACHE.estimating:
            return CACHE.active[backdoor]

        if backdoor in CACHE.canceled:
            _, estimation = CACHE.estimated[backdoor]
            return VoidHandle({**estimation, 'job_time': 0})

        if backdoor in CACHE.estimated:
            _, estimation = CACHE.estimated[backdoor]
            return VoidHandle({**estimation, 'job_time': 0})

        seeds = {
            'list_seed': self.random_state.randint(0, 2 ** 31),
            'func_seed': self.random_state.randint(0, 2 ** 32 - 1)
        }

        self.job_counter += 1
        return Job(Context(
            seeds,
            backdoor,
            self.instance,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
        ), self.job_counter).start()


__all__ = [
    'Estimator'
]
