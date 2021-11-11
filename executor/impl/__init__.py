from .thread_executor import *
from .process_executor import *
from .process_mpi_executor import *

executors = {
    ThreadExecutor.slug: ThreadExecutor,
    ProcessExecutor.slug: ProcessExecutor,
    ProcessMPIExecutor.slug: ProcessMPIExecutor
}
