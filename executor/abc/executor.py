from ..model import FutureAll

from typing import Callable
from typings.future import Future


class Executor:
    slug = 'executor'

    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        # using only for submit_all utilisation tracking
        self._trackers = []

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        raise NotImplementedError

    def submit_all(self, fn: Callable, *iterables) -> FutureAll:
        # for iterable in iterables:
        #     print(iterable)
        # print('iterables')
        # for args in zip(*iterables):
        #     print(args)
        # print('zip iterables')
        return FutureAll([
            self.submit(fn, *args) for args in iterables
        ]).append_tracker_to(self._trackers)

    # todo: implement executor.free()
    # def free(self):
    #     raise NotImplementedError

    def shutdown(self, wait: bool = True):
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'max_workers': self.max_workers,
        }


__all__ = [
    'Future',
    'Callable',
    'Executor',
    'FutureAll',
]
