from .mpi_executor import *
from .thread_executor import *
from .process_executor import *
from .thread_mpi_executor import *
from .process_mpi_executor import *

executors = {
    MPIExecutor.slug: MPIExecutor,
    ThreadExecutor.slug: ThreadExecutor,
    ProcessExecutor.slug: ProcessExecutor,
    ThreadMPIExecutor.slug: ThreadMPIExecutor,
    ProcessMPIExecutor.slug: ProcessMPIExecutor
}
