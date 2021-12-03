from ..function import *

from os import getpid
from time import time as now, sleep
from utils.array import concat
from utils import numeral_system as ns


def gad_task(i, solver, instance, data, key=None):
    st_timestamp = now()
    data_bits = decode_bits(data)
    simple_bd = instance.prepare_simple_bd(*data_bits[:2])
    assumptions = instance.get_assumptions(simple_bd, data_bits[2:])

    status, stats, _, _ = solver.solve(instance.clauses(), assumptions, key=key)
    result = (i, getpid(), status, stats, (st_timestamp, now()))
    return encode_result(result)


class GuessAndDetermine(Function):
    type = 'gad'
    name = 'Function: Guess-and-Determine'

    def get_job(self, backdoor: Backdoor, *dimension, **kwargs) -> Job:
        tasks, bd_bits, ad_bits = [], self.instance.get_bd_bits(backdoor), []
        if self.instance.has_intervals():
            clauses = self.instance.clauses()
            assumptions = self.instance.secret_key.values(rs=kwargs['random_state'])
            _, _, solution, _ = self.solver.solve(clauses, assumptions)

            for i, interval in enumerate(self.instance.intervals()):
                ad_bits.append(interval.get_bits(solution=solution))

        for i, values in enumerate(dimension):
            bits = concat(*ns.base_to_binary(self.instance.base + 1, *values))
            task_data = encode_bits([*bd_bits, bits, *ad_bits])
            tasks.append((i, self.solver, self.instance, task_data))
        return gad_task, tasks

    def calculate(self, backdoor: Backdoor, *cases: Case) -> Result:
        statistic = {True: 0, False: 0, None: 0}
        process_time, time_sum, value_sum = 0, 0, 0
        for case in cases:
            statistic[case[2]] += 1
            time_sum += case[3]['time']
            value_sum += self.measure.get(case[3])
            process_time += case[4][1] - case[4][0]

        time, value, = None, None
        count = backdoor.real_task_count()
        if count == len(cases):
            time, value = time_sum, value_sum
        elif len(cases) > 0:
            time = float(time_sum) / len(cases) * count
            value = float(value_sum) / len(cases) * count

        return statistic, {
            'time': time,
            'value': value,
            'count': len(cases),
            'job_time': time_sum,
            'process_time': process_time
        }


__all__ = [
    'GuessAndDetermine'
]
