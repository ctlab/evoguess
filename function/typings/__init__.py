from typing import Optional
from collections.abc import Callable

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure

ProcessId = int
ProcessTime = float

TaskId = int
TaskTime = float
TaskValue = float
TaskStatus = Optional[bool]

BackdoorBytes = bytes

Payload = tuple[
    Instance,  # instance = cnf
    Solver,
    Measure,
    BackdoorBytes,
    # todo: parse cnf intervals in process runtime
]

Result = tuple[
    ProcessId,
    ProcessTime,
    TaskId,
    TaskTime,
    TaskValue,
    TaskStatus
]

WorkerCallable = Callable[
    [list[TaskId], Payload],
    list[Result]
]

Estimation = dict

__all__ = [
    'TaskId',
    'Result',
    'Payload',
    'Estimation',
    'WorkerCallable',
]
