from typing import Optional
from collections.abc import Callable

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure
from instance.typings.variables.backdoor import Backdoor

ProcessId = int
ProcessTime = float

TaskIndex = int
TaskTime = float
TaskValue = float
TaskStatus = Optional[bool]

BackdoorBytes = bytes

Tasks = list[TaskIndex]
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
    TaskIndex,
    TaskTime,
    TaskValue,
    TaskStatus
]
Results = list[Result]

WorkerCallable = Callable[
    [Tasks, Payload],
    Results
]

Estimation = dict


class Function:
    type = None
    slug = 'function'
    name = 'Function'

    def __init__(self, solver, measure, *args, **kwargs):
        self.solver = solver
        self.measure = measure

    def get_payload(self, instance: Instance, backdoor: Backdoor) -> Payload:
        return (
            instance,
            self.solver,
            self.measure,
            backdoor.pack()
        )

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        raise NotImplementedError

    def get_function(self) -> WorkerCallable:
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'solver': self.solver.__info__(),
            'measure': self.measure.__info__(),
        }


__all__ = [
    'Function',
    # types
    'Tasks',
    'Payload',
    'Results',
    'Instance',
    'Backdoor',
    'Estimation',
    'WorkerCallable',
]
