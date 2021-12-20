from numpy.random import RandomState

from core.static import CACHE
from util.bitmask import to_bit
from util.collection import pick_by


class Context:
    def __init__(self, seeds, backdoor, instance, **kwargs):
        self.seeds = seeds
        self.backdoor = backdoor
        self.instance = instance

        self.space = kwargs.get('space')
        self.function = kwargs.get('function')
        self.sampling = kwargs.get('sampling')
        self.executor = kwargs.get('executor')
        # self.observer = kwargs.get('observer')

        self.sequence = None
        self.size = len(backdoor)
        self.base = backdoor.base
        self.power = backdoor.task_count()
        self.dim_type = to_bit(self.power > self.sampling.max_size)

    def _get_sequence(self):
        if self.sequence is None:
            if self.sampling.order == self.sampling.RANDOM:
                rs = RandomState(seed=self.seeds['list_seed'])
                self.sequence = rs.permutation(self.power)
            elif self.sampling.order == self.sampling.DIRECT:
                self.sequence = list(range(self.power))
            elif self.sampling.order == self.sampling.REVERSED:
                self.sequence = list(range(self.power))[::-1]
        return self.sequence

    def get_tasks(self, results):
        tasks, offset = [], len(results)
        values = self.sampling.get_values(results)
        count = self.sampling.get_count(self.backdoor, values)

        if count > 0:
            if self.dim_type:
                value = self.seeds['list_seed']
                tasks = [(i, value + i) for i in range(offset, offset + count)]
            else:
                values = self._get_sequence()
                tasks = [(i, values[i]) for i in range(offset, offset + count)]
        return tasks

    def get_estimation(self, results=None):
        del CACHE.estimating[self.backdoor]
        if results is None:
            CACHE.canceled[self.backdoor] = self.seeds
            return {**self.seeds, 'canceled': True}

        picked = pick_by(results)
        estimation = CACHE.estimated[self.backdoor] = {
            **self.seeds,
            'accuracy': len(picked) / len(results),
            **self.function.calculate(self.backdoor, *picked),
        }
        return estimation

    def get_limits(self, values, offset):
        return 0, None

    def is_reasonably(self, futures, values):
        return True


__all__ = [
    'Context'
]
