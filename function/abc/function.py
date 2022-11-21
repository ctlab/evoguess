from ..module.measure import Measure
from ..typings import WorkerArgs, WorkerResult, WorkerCallable, \
    Payload, Results, TimeMap, ValueMap, StatusMap, Estimation

from typing import Tuple

from core.module.space import Space
from function.module.solver import Solver
from instance.impl.instance import Instance
from instance.module.variables import Backdoor


def aggregate_results(results: Results) -> Tuple[TimeMap, ValueMap, StatusMap, int]:
    all_times, all_values, all_statuses = {}, {}, {}
    for _, _, times, values, statuses, _ in results:
        for status, time in times.items():
            all_times[status] = all_times.get(status, 0.) + time
        for status, value in values.items():
            all_values[status] = all_values.get(status, 0.) + value
        for status, count in statuses.items():
            all_statuses[status] = all_statuses.get(status, 0) + count
    return all_times, all_values, all_statuses, sum(all_statuses.values())


class Function:
    slug = 'function'
    supbs_required = False

    def __init__(self, solver: Solver, measure: Measure):
        self.solver = solver
        self.measure = measure

    def get_worker_fn(self) -> WorkerCallable:
        raise NotImplementedError

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        raise NotImplementedError

    def get_payload(self, space: Space, instance: Instance, backdoor: Backdoor) -> Payload:
        return space, self.solver, self.measure, instance, backdoor.pack()

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'solver': self.solver.__info__(),
            'measure': self.measure.__info__(),
        }


__all__ = [
    'Function',
    # types
    'Payload',
    'Results',
    'Estimation',
    'WorkerArgs',
    'WorkerResult',
    'WorkerCallable',
    # utils
    'aggregate_results'
]
