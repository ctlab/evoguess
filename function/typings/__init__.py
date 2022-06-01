from . import worker_t
from .worker_t import *

from typing import Any, Callable
from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure

# todo: import from backdoor
BackdoorBytes = bytes

Payload = tuple[
    Solver,
    Measure,
    Instance,  # instance = cnf
    BackdoorBytes,
    # todo: parse cnf intervals in process runtime
]

WorkerCallable = Callable[
    [WorkerArgs, Payload],
    WorkerResult
]

Results = list[ChunkResult]
Estimation = dict[str, Any]

__all__ = [
    'Results',
    'Payload',
    'Estimation',
    'WorkerCallable',
    *worker_t.__all__,
]
