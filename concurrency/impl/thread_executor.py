from .executor import *

from concurrent.futures.thread import ThreadPoolExecutor


class ThreadExecutor(Executor):
    name = "Concurrency: Thread Executor"

    def __init__(self, threads, *args, **kwargs):
        self.threads = threads
        super().__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=threads)

    def __len__(self):
        return self.threads

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            '-- Threads %d' % self.threads,
            '-- Seed: %s' % self.random_seed,
            '-- Tick: %.2f' % self.tick,
            '-- Workload: %.2f' % self.workload,
        ]))


__all__ = [
    'ThreadExecutor'
]
