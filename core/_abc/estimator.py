from ..static import *
from .._abc.core import *
from ..model.job import Job
from ..model.handle import *
from ..model.contex import Context


class Estimator(Core):
    def __init__(self, space, sampling, function, comparator, *args, **kwargs):
        self.space = space
        self.sampling = sampling
        self.function = function
        super().__init__(*args, **kwargs)

        CORE_CACHE.canceled = {}
        CORE_CACHE.estimated = {}
        CORE_CACHE.estimating = {}
        POINT_FACTORY.configure(comparator)

    def launch(self, *args, **kwargs):
        raise NotImplementedError

    def estimate(self, backdoor) -> Handle:
        if backdoor in CORE_CACHE.estimating:
            return CORE_CACHE.estimating[backdoor]

        # todo: is singleton justified?
        point = POINT_FACTORY.produce(backdoor)
        if backdoor in CORE_CACHE.canceled:
            _, estimation = CORE_CACHE.canceled[backdoor]
            return VoidHandle(point.set(**estimation))

        if backdoor in CORE_CACHE.estimated:
            _, estimation = CORE_CACHE.estimated[backdoor]
            return VoidHandle(point.set(**estimation))

        self.job_counter += 1
        job = Job(Context(
            backdoor,
            self.instance,
            space=self.space,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
            job_seed=self.random_state.randint(0, 2 ** 31 - 1)
        ), self.job_counter).start()
        handle = JobHandle(point, job)
        CORE_CACHE.active[backdoor] = handle

        return handle


__all__ = [
    'Estimator'
]
