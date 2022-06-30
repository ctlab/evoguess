from .._abc.function import *

from os import getpid
from time import time as now
from util.array import side_trim
from numpy.random.mtrand import RandomState


def ibs_function(common_data, tasks_data=None):
    inst, slv, meas, limits, payload = common_data

    bits = decode_bits(payload)
    dim_type, mask = bits[0], bits[1:]
    backdoor = inst.get_backdoor(mask=mask)

    results = []
    for task_data in tasks_data:
        st_timestamp = now()
        task_i, task_value = task_data
        # todo: provide uniq seed
        state = RandomState(seed=task_value)
        assumptions, constraints = \
            inst.get_supplements(slv, state, backdoor=backdoor)

        # print(task_i, repr(backdoor), assumptions, constraints)
        kwargs = {'limits': limits, 'constraints': constraints}
        status, stats, _ = slv.solve(inst, assumptions, **kwargs)
        time, value = stats['time'], meas.get(stats)
        results.append((task_i, getpid(), value, time, status, now() - st_timestamp))

    return results


class InverseBackdoorSets(Function):
    type = 'ibs'
    slug = 'function:ibs'
    name = 'Function: Inverse Backdoor Sets'

    def __init__(self, *args, **kwargs):
        limits = {
            'time_limit': kwargs.get('time_limit', 0),
            'conf_budget': kwargs.get('conf_budget', 0),
            'prop_budget': kwargs.get('prop_budget', 0)
        }
        assert sum(value != 0 for value in limits.values()) == 1, \
            "Define ONLY one of time_limit, conf_budget or prop_budget"
        for limit_key, limit_value in limits.items():
            if limit_value != 0:
                self.limit_key = limit_key
                self.limit_value = limit_value
                break

        self.min_xi = kwargs.get('min_xi', 0)
        super().__init__(*args, **kwargs)

    def get_function(self):
        return ibs_function

    def prepare_data(self, state, instance, backdoor, dim_type):
        assert instance.supbs is not None, "IBS method depends on instance supbs"
        assert instance.output_set is not None, "IBS method depends on instance output_set"

        bd_mask = side_trim(backdoor.get_mask(), at_start=False)
        return instance, self.solver, self.measure, {
            self.limit_key: self.limit_value
        }, encode_bits([*to_bits(dim_type, 1), *bd_mask])

    def calculate(self, backdoor, *cases):
        process_time, time_sum = 0, 0
        statistic = {True: 0, False: 0, None: 0}

        for case in cases:
            time_sum += case[3]
            process_time += case[5]
            statistic[case[4]] += 1

        time, value, = None, None
        if len(cases) > 0:
            xi = float(statistic[True] + statistic[False]) / float(len(cases))
            if xi > self.min_xi:
                value = (2 ** len(backdoor)) * self.limit_value * (3 / xi)
            else:
                value = float('inf')
            time = value if self.limit_key == 'time_limit' else None

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'statistic': statistic,
            'limit_key': self.limit_key,
            'job_time': round(time_sum, 2),
            'limit_value': self.limit_value,
            'process_time': round(process_time, 2),
        }

    def __info__(self):
        return {
            **super().__info__(),
            'min_xi': self.min_xi,
            'limit_key': self.limit_key,
            'limit_value': self.limit_value
        }


__all__ = [
    'InverseBackdoorSets'
]
