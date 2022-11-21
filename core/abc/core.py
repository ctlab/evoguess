from typing import Any

from output import Logger
from executor import Executor
from instance import Instance

from ..static import DEBUGGER

from typings.optional import Int
from numpy.random import randint, RandomState


class Core:
    slug = None

    def __init__(self,
                 logger: Logger,
                 instance: Instance,
                 executor: Executor,
                 random_seed: Int = None):
        self.logger = logger
        self.executor = executor
        self.instance = instance

        DEBUGGER.initialize(logger)
        self.random_seed = random_seed or randint(2 ** 32 - 1)
        self.random_state = RandomState(seed=self.random_seed)

    def launch(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def __config__(self):
        return {
            'instance': self.instance.__config__(),
            'executor': self.instance.__config__(),
            'random_seed': self.random_seed,
        }


__all__ = [
    'Core'
]
