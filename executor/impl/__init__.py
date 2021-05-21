from .thread_executor import *
from .process_executor import *

executors = {
    ThreadExecutor.slug: ThreadExecutor,
    ProcessExecutor.slug: ProcessExecutor,
}
