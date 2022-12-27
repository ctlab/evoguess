from .._abc.executor import *

from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor


class ThreadExecutor(Executor):
    slug = 'executor:thread'
    name = 'Executor: Thread'

    awaiter_dict = {
        'as_completed': as_completed,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=self.workers)

    def submit(self, fn: Callable, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)


__all__ = [
    'ThreadExecutor'
]
