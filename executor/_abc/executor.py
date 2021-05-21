from os import cpu_count
from numpy.random import randint, RandomState

from util.array import unzip


def multi_func(f, tasks):
    return [f(*args) for args in tasks]


class Executor:
    slug = 'executor'
    name = 'Executor'
    awaiter_dict = {}

    def __init__(self, shaping, **kwargs):
        self.shaping = shaping

        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.workers = kwargs.get('workers', cpu_count())
        self.random_state = RandomState(seed=self.seed)

    def submit(self, fn, task):
        raise NotImplementedError

    def submit_all(self, fn, *tasks):
        index_futures = []
        s_seed = self.random_state.randint(0, 2 ** 31 - 1)
        for shape in self.shaping.get(self.workers, tasks, seed=s_seed):
            index, future_tasks = unzip(shape)
            future = self.submit(multi_func, (fn, future_tasks))
            index_futures.append((index, future))
        return index_futures

    def get_awaiter(self, key='as_completed'):
        return self.awaiter_dict.get(key)

    def shutdown(self, wait=True):
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
    'Executor'
]
