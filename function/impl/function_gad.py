from .._abc.function import *

from os import getpid
from time import time as now
from numpy.random import RandomState


def gad_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    solver, measure, instance, _bytes = payload
    sample_seed, sample_size, offset, length = args
    timestamp, backdoor = now(), Backdoor.unpack()

    state = RandomState(sample_seed)

    if backdoor.task_count() == sample_size:
        sequence = state.permutation(sample_size)
        sequence = sequence[offset:offset + length]
        assumption_set = decimal_to_base(sequence, backdoor)
    else:
        # todo: make to chunk random sampling module?
        assumption_set = []

    times, values, statuses = {}, {}, {}
    for assumption_bits in assumption_set:
        # assumptions, constraints = instance.get_supplements()
        status, stats, _ = solver.solve(instance, assumptions, limit=measure.limits())
        time, (value, status) = stats['time'], measure.check_and_get(stats, status)

        times[status] = times.get(status, 0.) + time
        values[status] = values.get(status, 0.) + value
        statuses[status] = statuses.get(status, 0) + 1

    # todo: (optimize) dumps dict to str?
    return times, values, statuses, args, getpid(), timestamp - now()


class GuessAndDetermine(Function):
    slug = 'function:gad'

    def get_worker_fn(self) -> WorkerCallable:
        return gad_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        time, value, task_count = None, None, backdoor.task_count()
        ptime_sum, time_sum, value_sum, status_map = self._aggregate(results)

        if len(results) == task_count:
            time, value = time_sum, value_sum
        elif len(results) > 0:
            time = float(time_sum) / len(results) * task_count
            value = float(value_sum) / len(results) * task_count

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
    'GuessAndDetermine',
    *typings.__all__,
]
