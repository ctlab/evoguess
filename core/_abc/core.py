from executor import Executor
from numpy.random import randint, RandomState

from ..module.limitation import Limitation


class Core:
    slug = None
    name = 'Core'

    def __init__(self,
                 output,
                 instance,
                 executor: Executor,
                 limitation: Limitation,
                 *args, **kwargs):
        self.output = output
        self.executor = executor
        self.instance = instance
        self.limitation = limitation

        self.job_counter = 0
        self.start_stamp = None
        self.random_seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.random_seed)
        super().__init__(*args, **kwargs)

    def launch(self, *args, **kwargs):
        raise NotImplementedError


__all__ = [
    'Core'
]
