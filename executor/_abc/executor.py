from os import cpu_count
from typing import Callable

from numpy.random import randint, RandomState


class Executor:
    slug = 'executor'
    name = 'Executor'
    awaiter_dict = {}

    def __init__(self, shaping, **kwargs):
        self.shaping = shaping

        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.workers = kwargs.get('workers', cpu_count())
        self.random_state = RandomState(seed=self.seed)

    def submit(self, fn: Callable, *args, **kwargs):
        raise NotImplementedError

    def submit_all(self, fn, data, *tasks):
        index_futures = []
        for shape in self.shaping.get(self.workers, tasks):
            index = [task[0] for task in shape]
            future = self.submit(fn, data, shape)
            index_futures.append((index, future))
        return index_futures

    def get_awaiter(self, key='as_completed'):
        return self.awaiter_dict.get(key)

    def shutdown(self, wait: bool = True):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __len__(self):
        return self.workers

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'seed': self.seed,
            'workers': self.workers,
            'shaping': self.shaping.__info__(),
        }


__all__ = [
    'Callable',
    'Executor',
]
