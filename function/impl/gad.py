from .._abc.function import *

from os import getpid
from time import time as now
from util import array, numeral


def gad_function(i, solver, instance, data, key=None):
    st_timestamp = now()
    data_bits = decode_bits(data)
    simple_bd = instance.prepare_simple_bd(*data_bits[:2])
    assumptions = instance.get_assumptions(simple_bd, data_bits[2:])

    status, stats, _ = solver.solve(instance.clauses(), assumptions, key=key)
    result = (i, getpid(), status, stats, (st_timestamp, now()))
    # todo: reformat results
    return result
    return destruct_result(result)


class GuessAndDetermine(Function):
    type = 'gad'
    slug = 'function:gad'
    name = 'Function: Guess-and-Determine'

    def get_function(self):
        return gad_function

    def prepare_tasks(self, instance, backdoor, *dimension, **kwargs):
        tasks, bd_bits, ad_bits = [], instance.get_bd_bits(backdoor), []
        if instance.has_intervals():
            clauses = instance.clauses()
            # todo: fix for domain variables
            assumptions = instance.secret_key.values(seed=kwargs['seed'])
            _, _, solution = self.solver.solve(clauses, assumptions)

            # todo: consider base for ad_bits
            # for i, interval in enumerate(_instance.intervals()):
            #     ad_bits.append(interval.get_bits(solution=solution))

        for i, values in enumerate(dimension):
            bits = array.concat(*numeral.base_to_binary(backdoor.base + 1, *values))
            task_data = encode_bits([*bd_bits, bits, *ad_bits])
            tasks.append((i, self.solver, instance, task_data))
        return tasks

    def calculate(self, backdoor, *cases):
        statistic = {True: 0, False: 0, None: 0}
        process_time, time_sum, value_sum = 0, 0, 0
        for case in cases:
            statistic[case[2]] += 1
            time_sum += case[3]['time']
            value_sum += self.measure.get(case[3])
            process_time += case[4][1] - case[4][0]

        time, value, = None, None
        count = backdoor.task_count()
        if count == len(cases):
            time, value = time_sum, value_sum
        elif len(cases) > 0:
            time = float(time_sum) / len(cases) * count
            value = float(value_sum) / len(cases) * count

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'job_time': time_sum,
            'process_time': process_time,
            'statistic': statistic
        }


__all__ = [
    'GuessAndDetermine'
]
