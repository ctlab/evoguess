from . import worker_t
from .worker_t import *

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure
from typing import Any, Callable, List, Dict, Tuple

# todo: import from backdoor
BackdoorBytes = bytes

Payload = Tuple[
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

Results = List[ChunkResult]
Estimation = Dict[str, Any]

__all__ = [
    'Results',
    'Payload',
    'Estimation',
    'WorkerCallable',
    *worker_t.__all__,
]
