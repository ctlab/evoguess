from numpy.random import RandomState

from util.bitmask import to_bit
from util.collection import trim


class Context:
    def __init__(self, seeds, instance, backdoor, **kwargs):
        self.seeds = seeds
        self.instance = instance
        self.backdoor = backdoor

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
        count = self.sampling.get_count(self.backdoor, results)

        if count > 0:
            if self.dim_type:
                value = self.seeds['list_seed']
                tasks = [(i, value + i) for i in range(offset, offset + count)]
            else:
                values = self._get_sequence()
                tasks = [(i, values[i]) for i in range(offset, offset + count)]
        return tasks

    def get_estimation(self, results=None):
        trimmed = trim(results)
        return {
            'list_seed': self.seeds['list_seed'],
            'func_seed': self.seeds['func_seed'],
            'accuracy': len(trimmed) / len(results),
            **self.function.calculate(self.backdoor, *trimmed),
        }

    def get_limits(self, values, offset):
        return 0, None

    def is_reasonably(self, futures, values):
        return True


__all__ = [
    'Context'
]
