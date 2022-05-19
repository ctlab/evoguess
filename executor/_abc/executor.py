from ..model import *

from os import cpu_count


class Executor:
    slug = 'executor'
    name = 'Executor'

    def __init__(self, *args, **kwargs):
        self.workers = kwargs.get('workers', cpu_count())
        # todo: add executor.free()

    def submit(self, fn, *args, **kwargs):
        raise NotImplementedError

    # def submit_all(self, fn, *args, **kwargs) -> FutureAll:
    #     # todo: rewrite this method
    #     futures = []
    #     for args, kwargs in argslist:
    #         #     index = [task.index for task in shape]
    #         future = self.submit(fn, *args, *gargs, **gkwargs, **kwargs)
    #     #     index_futures.append((index, future))
    #     return FutureAll(futures)

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
            'workers': self.workers,
        }


__all__ = [
    'Executor',
    'FutureAll'
]
