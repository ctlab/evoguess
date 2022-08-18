from ..model import FutureAll

from os import cpu_count
from typing import Callable
from typings.future import Future


class Executor:
    slug = 'executor'

    def __init__(self, *args, **kwargs):
        self.workers = kwargs.get('workers', cpu_count())
        # using only for submit_all utilisation tracking
        self._trackers = []

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        raise NotImplementedError

    def submit_all(self, fn: Callable, *iterables) -> FutureAll:
        return FutureAll([
            self.submit(fn, *args)
            for args in zip(*iterables)
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
            'workers': self.workers,
        }


__all__ = [
    'Future',
    'Callable',
    'Executor',
    'FutureAll',
]
