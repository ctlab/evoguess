from ..abc.executor import *

from os import cpu_count
from concurrent.futures.thread import ThreadPoolExecutor


class ThreadExecutor(Executor):
    slug = 'executor:thread'

    def __init__(self, workers: int = None):
        super().__init__(workers=workers or cpu_count())
        self.executor = ThreadPoolExecutor(max_workers=self.workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        self.executor.shutdown(wait)


__all__ = [
    'ThreadExecutor'
]
