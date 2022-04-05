from . import task_result
from .task_result import *
from collections.abc import Callable

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure

# todo: import from backdoor
BackdoorBytes = bytes

Payload = tuple[
    Instance,  # instance = cnf
    Solver,
    Measure,
    BackdoorBytes,
    # todo: parse cnf intervals in process runtime
]

WorkerCallable = Callable[
    [list[TaskId], Payload],
    list[Result]
]

Estimation = dict

__all__ = [
    'Payload',
    'Estimation',
    'WorkerCallable',
    *task_result.__all__,
]
