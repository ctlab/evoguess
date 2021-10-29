from .._abc.function import *

from os import getpid
from time import time as now
from numpy.random.mtrand import RandomState


def ibs_function(common_data, tasks_data=None):
    inst, slv, meas, tl, info = common_data

    results = []
    bits = decode_bits(info)
    [dim_type, bd_type] = bits[:2]
    bd_base = to_number(bits[2:8], 6)
    mask_len = to_number(bits[8:24], 16)
    bd_mask = bits[24:mask_len + 24]

    supbs_vars = inst.supbs.variables()
    backdoor = inst.get_backdoor2(bd_type, bd_base, bd_mask)
    as_vars = backdoor.variables() + inst.output_set.variables()

    with slv.prototype(inst.clauses()) as propagator:
        for task_data in tasks_data:
            st_timestamp = now()
            task_i, task_value = task_data

            # todo: provide uniq seed
            supbs_vars = inst.supbs.variables()
            state = RandomState(seed=task_value)

            i_values = state.randint(0, bd_base, size=len(supbs_vars))
            i_assumptions = [x if i_values[i] else -x for i, x in enumerate(supbs_vars)]
            _, _, literals = propagator.propagate(i_assumptions)

            assumptions = []
            bd_vars = backdoor.variables()
            for lit in literals:
                if abs(lit) in as_vars:
                    assumptions.append(lit)

            status, stats, _ = slv.solve(inst.clauses(), assumptions, limit=tl)
            time, value = stats['time'], meas.get(stats)
            results.append((task_i, getpid(), value, time, status, now() - st_timestamp))

    return results


class InverseBackdoorSets(Function):
    type = 'ibs'
    slug = 'function:ibs'
    name = 'Function: Inverse Backdoor Sets'

    def __init__(self, time_limit, *args, **kwargs):
        self.time_limit = time_limit
        super().__init__(*args, **kwargs)

    def get_function(self):
        return ibs_function

    def prepare_data(self, state, instance, backdoor, dim_type):
        assert instance.supbs is not None, "IBS method depends on instance supbs"
        assert instance.output_set is not None, "IBS method depends on instance output_set"

        bd_mask = instance.get_bd_mask(backdoor)
        return instance, self.solver, self.measure, self.time_limit, encode_bits([
            *to_bits(dim_type, 1),
            *to_bits(backdoor.kind, 1),
            *to_bits(backdoor.base, 6),
            *to_bits(len(bd_mask), 16),
            *bd_mask
        ])

    def calculate(self, backdoor, *cases):
        statistic = {True: 0, False: 0, None: 0}
        process_time, time_sum, value_sum = 0, 0, 0

        for case in cases:
            time_sum += case[3]
            value_sum += case[2]
            process_time += case[5]
            statistic[case[4]] += 1

        xi = float(statistic[True] + statistic[False]) / float(len(cases))
        if xi != 0:
            time = value = (2 ** len(backdoor)) * self.time_limit * (3 / xi)
        else:
            time = value = float('inf')
            # value = (2 ** env.algorithm.secret_key_len) * self.time_limit

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'statistic': statistic,
            'job_time': round(time_sum, 2),
            'process_time': round(process_time, 2),
        }
