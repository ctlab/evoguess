from .._abc.function import *

from os import getpid
from time import time as now


def ibs_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    solver, measure, instance, _bytes = payload
    sample_seed, sample_size, offset, length = args
    timestamp, backdoor = now(), Backdoor.unpack()

    times, values, statuses = {}, {}, {}
    return times, values, statuses, args, getpid(), timestamp - now()


class InverseBackdoorSets(Function):
    slug = 'function:ibs'
    supbs_required = True

    def get_worker_fn(self) -> WorkerCallable:
        return ibs_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        time, value, task_count = None, None, backdoor.task_count()
        ptime_sum, time_sum, value_sum, status_map = self._aggregate(results)

        solved_count = status_map[True] + status_map[False]
        if solved_count > 0:
            xi = float(solved_count) / len(results)
            value = task_count * self.measure.budget * (3 / xi)
            time = value if self.measure.key == 'time' else None
        elif len(results) > 0:
            time, value = float('inf'), float('inf')

        return {
            'time': time,
            'value': value,
            'count': len(results),
            'status_map': status_map,
            'job_time': round(time_sum, 2),
            'job_value': round(value_sum, 2),
            'process_time': round(ptime_sum, 2)
        }


__all__ = [
    'InverseBackdoorSets',
    *typings.__all__,
]
