from .._abc.core import *
from ..static import CACHE, FACTORY

from ..typings.job import Job
from ..typings.contex import Context
from ..typings.handle import VoidHandle, JobHandle, Handle


class Estimator(Core):
    def __init__(self, space, sampling, function, comparator, *args, **kwargs):
        self.space = space
        self.sampling = sampling
        self.function = function
        super().__init__(*args, **kwargs)

        CACHE.canceled = {}
        CACHE.estimated = {}
        CACHE.estimating = {}
        FACTORY.set(comparator)

    def launch(self, *args, **kwargs):
        raise NotImplementedError

    def estimate(self, backdoor) -> Handle:
        if backdoor in CACHE.estimating:
            return CACHE.estimating[backdoor]

        # todo: is singleton justified?
        point = FACTORY.produce(backdoor)
        if backdoor in CACHE.canceled:
            _, estimation = CACHE.canceled[backdoor]
            return VoidHandle(point.set(**estimation))

        if backdoor in CACHE.estimated:
            _, estimation = CACHE.estimated[backdoor]
            return VoidHandle(point.set(**estimation))

        seeds = {
            'list_seed': self.random_state.randint(0, 2 ** 31),
            'func_seed': self.random_state.randint(0, 2 ** 32 - 1)
        }

        self.job_counter += 1
        job = Job(Context(
            seeds,
            backdoor,
            self.instance,
            space=self.space,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
        ), self.job_counter).start()
        handle = JobHandle(point, job)
        CACHE.active[backdoor] = handle

        return handle


__all__ = [
    'Estimator'
]
