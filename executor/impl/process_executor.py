from .._abc.executor import *

from concurrent.futures.process import ProcessPoolExecutor


class ProcessExecutor(Executor):
    slug = 'executor:process'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = ProcessPoolExecutor(max_workers=self.workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        self.executor.shutdown(wait)


__all__ = [
    'ProcessExecutor'
]
