from .._abc.executor import *

try:
    from mpi4py import MPI
    from mpi4py.futures import as_completed
    from mpi4py.futures.pool import ProcessPoolExecutor
except ModuleNotFoundError:
    as_completed = None


class ProcessMPIExecutor(Executor):
    slug = 'executor:process:mpi'
    name = "Executor: Process MPI"

    awaiter_dict = {
        'as_completed': as_completed,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mpi_size = MPI.COMM_WORLD.Get_size()
        self.workers = max(1, self.mpi_size - 1)
        self.executor = ProcessPoolExecutor(max_workers=self.workers)

    def submit(self, fn: Callable, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)


__all__ = [
    'ProcessMPIExecutor'
]
