from .._abc.function import *


def ibs_function(tasks: Tasks, payload: Payload) -> Results:
    instance, solver, measure, _bytes = payload
    backdoor = Backdoor.unpack(_bytes)

    return []


class InverseBackdoorSets(Function):
    slug = 'function:ibs'
    name = 'Function: Inverse Backdoor Sets'

    def get_function(self) -> WorkerCallable:
        return ibs_function

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
    # types
    'Tasks',
    'Payload',
    'Results',
    'Instance',
    'Backdoor',
    'Estimation',
    'WorkerCallable',
]
