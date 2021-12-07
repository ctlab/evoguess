from .._abc.executor import *

from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor


class ProcessExecutor(Executor):
    slug = 'executor:process'
    name = "Executor: Process"

    awaiter_dict = {
        'as_completed': as_completed,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ProcessPoolExecutor(max_workers=self.workers)

    def submit(self, fn: Callable, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)


__all__ = [
    'ProcessExecutor'
]
