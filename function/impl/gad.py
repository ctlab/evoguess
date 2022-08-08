from .._abc.function import *

from os import getpid
from time import time as now
from util.array import side_trim
from instance.typings.var import compress
from numpy.random.mtrand import RandomState


def gad_function(common_data, tasks_data=None):
    inst, slv, meas, payload = common_data

    bits = decode_bits(payload)
    dim_type, mask = bits[0], bits[1:]
    backdoor = inst.get_backdoor(mask=mask)
    assumptions, constraints = inst.get_supplements(slv)

    results = []
    var_bases = backdoor.get_var_bases()
    for task_data in tasks_data:
        st_timestamp = now()
        task_i, task_value = task_data

        if dim_type == NUMBERS:
            state = RandomState(seed=task_value)
            values = state.randint(0, var_bases)
        else:
            values = decimal_to_base(task_value, var_bases)

        task_values = {
            var: value for var, value in zip(backdoor, values)
        }
        task_assumptions, task_constraints = compress(*(
            var.supplements(task_values) for var in backdoor
        ))

        status, stats, _ = slv.solve(
            inst.encoding_data(), assumptions + task_assumptions,
            constraints=constraints + task_constraints
        )
        time, value = stats['time'], meas.get(stats)
        results.append((task_i, getpid(), value, time, status, now() - st_timestamp))

    return results


class GuessAndDetermine(Function):
    type = 'gad'
    slug = 'function:gad'
    name = 'Function: Guess-and-Determine'

    def get_function(self):
        return gad_function

    def prepare_data(self, state, instance, backdoor, dim_type):
        bd_mask = side_trim(backdoor.get_mask(), at_start=False)
        return instance, self.solver, self.measure, encode_bits([
            *to_bits(dim_type, 1), *bd_mask
        ])

    def calculate(self, backdoor, *cases):
        statistic = {True: 0, False: 0, None: 0}
        process_time, time_sum, value_sum = 0, 0, 0

        for case in cases:
            time_sum += case[3]
            value_sum += case[2]
            process_time += case[5]
            statistic[case[4]] += 1

        time, value, = None, None
        count = backdoor.power()
        if count == len(cases):
            time, value = time_sum, value_sum
        elif len(cases) > 0:
            time = float(time_sum) / len(cases) * count
            value = float(value_sum) / len(cases) * count

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'statistic': statistic,
            'job_time': round(time_sum, 2),
            'job_value': round(value_sum, 2),
            'process_time': round(process_time, 2)
        }


__all__ = [
    'GuessAndDetermine'
]
