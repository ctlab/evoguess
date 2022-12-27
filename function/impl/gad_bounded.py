from .._abc.function import *

from os import getpid
from time import time as now
from numpy.random.mtrand import RandomState


def gad_function(common_data, tasks_data=None):
    inst, slv, meas, limits, info = common_data

    results = []
    bits = decode_bits(info)
    [dim_type, bd_type] = bits[:2]
    bd_base = to_number(bits[2:8], 6)
    mask_len = to_number(bits[8:24], 16)
    bd_mask = bits[24:mask_len + 24]

    kwargs = {'limits': limits}
    if inst.cnf.has_atmosts and inst.cnf.atmosts():
        kwargs['atmosts'] = inst.cnf.atmosts()

    backdoor = inst.get_backdoor2(bd_type, bd_base, bd_mask)
    bases = backdoor.get_bases()

    extra_assumptions = []
    if inst.has_intervals():
        state = RandomState()
        supbs_vars = inst.supbs.variables()
        output_vars = inst.output_set.variables()
        supbs_values = state.randint(0, bd_base, size=len(supbs_vars))
        supbs_assumptions = [x if supbs_values[i] else -x for i, x in enumerate(supbs_vars)]
        _, _, solution = slv.solve(inst, supbs_assumptions)

        for lit in solution:
            if abs(lit) in output_vars:
                extra_assumptions.append(lit)

        assert len(extra_assumptions) == len(output_vars)

    for task_data in tasks_data:
        st_timestamp = now()
        task_i, task_value = task_data

        if dim_type == NUMBERS:
            state = RandomState(seed=task_value)
            values = state.randint(0, bd_base, size=len(backdoor))
            # todo: apply backdoor.get_masks() to values
        else:
            values = decimal_to_base(task_value, bases)
            # todo: map values using backdoor.get_mappers()

        assumptions = inst.get_assumptions(backdoor, values)
        status, stats, _ = slv.solve(inst, assumptions + extra_assumptions, **kwargs)
        time, value = stats['time'], meas.get(stats)
        results.append((task_i, getpid(), value, time, status, now() - st_timestamp))
    return results


class BoundedGuessAndDetermine(Function):
    type = 'gad'
    slug = 'function:gad_bounded'
    name = 'Function: Bounded Guess-and-Determine'

    def __init__(self, alpha_n, *args, **kwargs):
        limits = {
            'time_limit': kwargs.get('time_limit', 0),
            'conf_budget': kwargs.get('conf_budget', 0),
            'prop_budget': kwargs.get('prop_budget', 0)
        }
        self.alpha_n = alpha_n
        self.min_limit = kwargs.get('min_limit', 0)

        assert sum(value != 0 for value in limits.values()) == 1, \
            "Define ONLY one of time_limit, conf_budget or prop_budget"
        for limit_key, limit_value in limits.items():
            if limit_value != 0:
                self.limit_key = limit_key
                self.limit_value = limit_value
                break

        super().__init__(*args, **kwargs)

    def get_function(self):
        return gad_function

    def prepare_data(self, state, instance, backdoor, dim_type):
        bd_mask = instance.get_bd_mask(backdoor)
        return instance, self.solver, self.measure, {
            self.limit_key: self.limit_value
        }, encode_bits([
            *to_bits(dim_type, 1),
            *to_bits(backdoor.kind, 1),
            *to_bits(backdoor.base, 6),
            *to_bits(len(bd_mask), 16),
            *bd_mask
        ])

    def calculate(self, backdoor, *cases):
        rho_cases = 0
        process_time, time_sum = 0, 0
        statistic = {True: 0, False: 0, None: 0}

        for case in cases:
            time_sum += case[3]
            process_time += case[5]
            statistic[case[4]] += 1

            if case[4] is False and case[2] >= self.min_limit:
                rho_cases += 1

        if rho_cases > 0:
            count = backdoor.task_count()
            rho = float(rho_cases) / len(cases)
            value = rho * count + (1 - rho) * (2 ** self.alpha_n)
        else:
            value = float('inf')
        time = value if self.limit_key == 'time_limit' else None

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'rho_cases': rho_cases,
            'statistic': statistic,
            'limit_key': self.limit_key,
            'job_time': round(time_sum, 2),
            'limit_value': self.limit_value,
            'process_time': round(process_time, 2),
        }


__all__ = [
    'BoundedGuessAndDetermine'
]
