from ..typings.job import Job
from ..typings.handle import VoidHandle, JobHandle

import pylru
from util.bitmask import to_bit
from collections import namedtuple
from numpy.random import randint, RandomState

Cache = namedtuple('Cache', 'active canceled estimated')


class Method:
    slug = 'method'
    name = 'Method'

    def __init__(self, function, executor, sampling, **kwargs):
        self.function = function
        self.executor = executor
        self.sampling = sampling
        # self.observer = observer

        self.last_job_id = 0
        cache_size = kwargs.get('cache_size', 100_000)
        self._cache = Cache({}, {}, pylru.lrucache(cache_size))
        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.seed)

    def queue(self, instance, backdoor):
        if backdoor in self._cache.active:
            return self._cache.active[backdoor]

        if backdoor in self._cache.canceled:
            _, estimation = self._cache.estimated[backdoor]
            return VoidHandle({**estimation, 'job_time': 0})

        if backdoor in self._cache.estimated:
            _, estimation = self._cache.estimated[backdoor]
            return VoidHandle({**estimation, 'job_time': 0})

        seeds = {
            'list_seed': self.random_state.randint(0, 2 ** 31),
            'func_seed': self.random_state.randint(0, 2 ** 32 - 1)
        }

        self.last_job_id += 1
        job = Job(Context(
            seeds,
            instance,
            backdoor,
            self._cache,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
            # observer=self.observer
        ), self.last_job_id).start()

        self._cache.active[backdoor] = JobHandle(job)
        return self._cache.active[backdoor]

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'seed': self.seed,
            'function': self.function.__info__(),
            'executor': self.executor.__info__(),
            'sampling': self.sampling.__info__(),
            # 'observer': self.observer.__info__()
        }

    def __str__(self):
        return self.name


__all__ = [
    'Method'
]
