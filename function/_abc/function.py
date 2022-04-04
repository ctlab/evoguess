from ..typings import *

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure
from instance.typings.variables.backdoor import Backdoor


class Function:
    slug = 'function'
    name = 'Function'

    def __init__(self, solver: Solver, measure: Measure, *args, **kwargs):
        self.solver = solver
        self.measure = measure

    def get_payload(self, instance: Instance, backdoor: Backdoor) -> Payload:
        return (
            instance,
            self.solver,
            self.measure,
            backdoor.pack()
        )

    def _aggregate(self, results: list[Result]) -> tuple[float, float, float, dict]:
        status_map = {True: 0, False: 0, None: 0}
        ptime_sum, time_sum, value_sum = 0, 0, 0
        for result in results:
            _, ptime, _, time, value, status = result
            time_sum += time
            ptime_sum += ptime
            value_sum += value
            status_map[status] += 1

        return ptime_sum, time_sum, value_sum, status_map

    def calculate(self, backdoor: Backdoor, results: list[Result]) -> Estimation:
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
    'TaskId',
    'Result',
    'Payload',
    'Instance',
    'Backdoor',
    'Estimation',
    'WorkerCallable',
]
