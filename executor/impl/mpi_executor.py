from .._abc.executor import *

try:
    from mpi4py import MPI
    from mpi4py.futures import MPIPoolExecutor
except ModuleNotFoundError:
    pass


class MPIExecutor(Executor):
    slug = 'executor:mpi'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mpi_size = MPI.COMM_WORLD.Get_size()
        self.workers = max(1, self.mpi_size - 1)
        self.executor = MPIPoolExecutor(max_workers=self.workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        self.executor.shutdown(wait)


__all__ = [
    'MPIExecutor'
]
