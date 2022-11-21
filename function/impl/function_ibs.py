from ..abc.function import *

from os import getpid
from typing import Iterable
from time import time as now

from instance import Instance
from instance.module.variables import Backdoor
from instance.module.variables.vars import Supplements


def ibs_supplements(args: WorkerArgs, instance: Instance,
                    backdoor: Backdoor) -> Iterable[Supplements]:
    # todo: add ibs_supplements realisation!
    return []


def ibs_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    preset = solver.preset(instance.encoding, measure)
    for supplements in ibs_supplements(args, instance, backdoor):
        time, status, value, _ = preset.solve(supplements, add_model=False)

        times[status] = times.get(status, 0.) + time
        values[status] = values.get(status, 0.) + value
        statuses[status] = statuses.get(status, 0) + 1
    # todo: (optimize) dumps dict to str?
    return getpid(), now() - timestamp, times, values, statuses, args


class InverseBackdoorSets(Function):
    slug = 'function:ibs'

    def get_worker_fn(self) -> WorkerCallable:
        return ibs_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        times, values, statuses, count = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, budget, value = backdoor.power(), self.measure.budget, float('inf')
        solved_count = sum(statuses[key] for key in ['SAT', 'UNSAT'])

        if solved_count > 0:
            xi = float(solved_count) / len(results)
            value = power * budget * (3 / xi)

        return {
            'value': value,
            'count': count,
            'statuses': statuses,
            'time_sum': round(time_sum, 4),
            'value_sum': round(value_sum, 4),
        }


__all__ = [
    'InverseBackdoorSets',
    # types
    # 'Payload',
    # 'Results',
    # 'WorkerArgs',
    # 'Estimation',
    # 'WorkerResult',
    # 'WorkerCallable'
]
