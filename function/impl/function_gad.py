from .._abc.function import *


def gad_function(tasks: list[TaskId], payload: Payload) -> list[Result]:
    instance, solver, measure, _bytes = payload
    backdoor = Backdoor.unpack(_bytes)

    return []


class GuessAndDetermine(Function):
    slug = 'function:gad'
    name = 'Function: Guess-and-Determine'

    def get_function(self) -> WorkerCallable:
        return gad_function

    def calculate(self, backdoor: Backdoor, results: list[Result]) -> Estimation:
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
    # types
    'TaskId',
    'Result',
    'Payload',
    'Instance',
    'Backdoor',
    'Estimation',
    'WorkerCallable',
]
