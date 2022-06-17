from .._abc.function import *

from os import getpid
from math import log2
from time import time as now
from util.array import side_trim
from instance.typings.var import compress
from numpy.random.mtrand import RandomState


def gad_function(common_data, tasks_data=None):
    inst, slv, meas, payload = common_data

    results = []
    bits = decode_bits(payload)
    dim_type, mask = bits[0], bits[1:]
    backdoor = inst.get_backdoor(mask=mask)
    assumptions, constraints = inst.get_supplements(slv)

    var_bases = backdoor.get_var_bases()
    with slv.prototype(inst) as solver:
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

            # todo: constraints with incremental propagation
            if len(task_constraints) > 0:
                status, stats, literals = None, {}, []
            else:
                status, stats, literals = solver.propagate(assumptions + task_assumptions)
            time, value = stats['time'], meas.get(stats)
            status = not (status and len(literals) < inst.max_literal())
            results.append((task_i, getpid(), value, time, status, now() - st_timestamp))

    return results


class UPGuessAndDetermine(Function):
    type = 'gad'
    slug = 'function:up_gad'
    name = 'Function: UP Guess-and-Determine'

    def __init__(self, max_n, *args, **kwargs):
        self.max_n = max_n
        self.alpha_n = kwargs.get('alpha_n', max_n)
        self.value_base = kwargs.get('value_base', 2)
        super().__init__(*args, **kwargs)

    def get_function(self):
        return gad_function

    def prepare_data(self, state, instance, backdoor, dim_type):
        bd_mask = side_trim(backdoor.get_mask(), at_start=False)
        return instance, self.solver, self.measure, encode_bits([
            *to_bits(dim_type, 1), *bd_mask
        ])

    def calculate(self, backdoor, *cases):
        process_time, time_sum = 0, 0
        statistic = {True: 0, False: 0}
        values_sum = {True: 0, False: 0}

        for case in cases:
            time_sum += case[3]
            process_time += case[5]
            statistic[case[4]] += 1
            values_sum[case[4]] += case[2]

        time, value, = None, None
        if len(cases) > 0:
            time = log2(float(time_sum) / len(cases)) + len(backdoor)
            if self.value_base < 2:
                count = self.value_base ** len(backdoor)
                vfp = float(statistic[True]) / len(cases)
                pfp = float(statistic[False]) / len(cases)
                value = vfp * count + pfp * (2 ** self.alpha_n)
            else:
                if len(backdoor) < self.max_n:
                    count = backdoor.power()
                    vfp = float(statistic[True]) / len(cases)
                    pfp = float(statistic[False]) / len(cases)
                    value = log2(vfp * count + pfp * (2 ** self.alpha_n))
                else:
                    if statistic[False] > 0:
                        value = float('inf')
                    else:
                        value = len(backdoor)
                        # value = sum(values_sum.values()) / len(cases)

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'statistic': statistic,
            'job_values': values_sum,
            'job_time': round(time_sum, 2),
            'process_time': round(process_time, 2),
        }

    def __info__(self):
        return {
            **super().__info__(),
            'max_n': self.max_n,
            'alpha_n': self.alpha_n,
        }


__all__ = [
    'UPGuessAndDetermine'
]
