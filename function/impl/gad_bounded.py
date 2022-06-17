from .._abc.function import *

from os import getpid
from time import time as now
from util.array import side_trim
from instance.typings.var import compress
from numpy.random.mtrand import RandomState


def gad_function(common_data, tasks_data=None):
    inst, slv, meas, limits, payload = common_data

    bits = decode_bits(payload)
    dim_type, mask = bits[0], bits[1:]
    backdoor = inst.get_backdoor(mask=mask)
    assumptions, constraints = inst.get_supplements(slv)

    results, kwargs = [], {'limits': limits}
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
            inst, assumptions + task_assumptions,
            constraints=constraints + task_constraints
        )
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
        bd_mask = side_trim(backdoor.get_mask(), at_start=False)
        return instance, self.solver, self.measure, {
            self.limit_key: self.limit_value
        }, encode_bits([*to_bits(dim_type, 1), *bd_mask])

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
            count = backdoor.power()
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
