from ..cache import Cache
from .._type.job import Job
from .._type.dimension import Dimension
from .._type.method_future import MethodFuture, EstimationFuture

from numpy.random import randint


class Context:
    def __init__(self, instance, backdoor, cache, **context):
        self.cache = cache
        self.instance = instance
        self.backdoor = backdoor

        self.function = context.get('function')
        self.sampling = context.get('sampling')
        self.executor = context.get('executor')
        self.observer = context.get('observer')

        # todo: refactor
        # dimension = Dimension(backdoor, cache)
        # self.dimension = iter(dimension)

    def get_tasks(self, cases, offset):
        values = self.function.get_values(*cases)
        count = self.sampling.get_count(self.backdoor, values=values)
        if count == 0:
            return []

        # todo: refactor
        dimension = iter(Dimension(self.backdoor, self.cache, len(values)))
        dimension = [next(dimension)[1] for _ in range(count)]
        f_seed = self.cache.state[self.backdoor].seeds.function_seed
        tasks = self.function.prepare_tasks(self.instance, self.backdoor, *dimension, seed=f_seed)

        return tasks

    def get_limits(self, cases, offset):
        return 0, None

    def is_reasonably(self, futures, cases):
        return True

class Method:
    slug = 'method'
    name = 'Method'

    def __init__(self, function, executor, sampling, observer, **kwargs):
        self.function = function
        self.executor = executor
        self.sampling = sampling
        self.observer = observer

        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self._cache = Cache(self.seed, *self.sampling.get_size())

    def queue(self, instance, backdoor):
        if backdoor in self._cache.active:
            return self._cache.active[backdoor]

        if backdoor in self._cache.canceled:
            _, estimation = self._cache.estimated[backdoor]
            return EstimationFuture(estimation)

        if backdoor in self._cache.estimated:
            _, estimation = self._cache.estimated[backdoor]
            return EstimationFuture(estimation)

        job = Job(Context(
            instance,
            backdoor,
            self._cache,
            function=self.function,
            sampling=self.sampling,
            executor=self.executor,
            observer=self.observer
        )).start()

        self._cache.active[backdoor] = MethodFuture(job)
        return self._cache.active[backdoor]

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'seed': self.seed,
            'function': self.function.__info__(),
            'sampling': self.sampling.__info__(),
        }

    def __str__(self):
        return self.name


__all__ = [
    'Method'
]
