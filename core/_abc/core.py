from executor import Executor
from instance import Instance

from typings.optional import Int
from ..module.limitation import Limitation
from numpy.random import randint, RandomState


class Core:
    slug = None
    name = 'Core'

    def __init__(self,
                 output,
                 instance: Instance,
                 executor: Executor,
                 limitation: Limitation,
                 random_seed: Int = None,
                 *args, **kwargs):
        self.output = output
        self.executor = executor
        self.instance = instance
        self.limitation = limitation

        self.random_seed = random_seed or randint(2 ** 32 - 1)
        self.random_state = RandomState(seed=self.random_seed)
        super().__init__(*args, **kwargs)

    def launch(self, *args, **kwargs):
        raise NotImplementedError


__all__ = [
    'Core'
]
