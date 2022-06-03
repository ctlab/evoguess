from .._abc.function import *

from os import getpid
from time import time as now
from itertools import compress
from util.numeral import base_to_binary2
from numpy.random.mtrand import RandomState

BENT_INDEXES = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
MAJ_INDEXES = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 61]
XOR_INDEXES = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44,
               46, 48, 50, 52, 54, 56, 58, 60, 62]


def xor(*args):
    return sum(args) % 2 == 1


def bent_4(x1, x2, x3, x4):
    return xor(x1 and x3, x2 and x4)


def majority(*args):
    return sum(args) > len(args) // 2


def get_constraints(operator, *args):
    clauses, size = [], len(args)
    result = operator(*(1 if arg > 0 else 0 for arg in args))
    for value in range(0, 2 ** size):
        bits = base_to_binary2(size, value)
        if operator(*bits) != result:
            clauses.append([
                -lit if bit else lit for
                lit, bit in zip(map(abs, args), bits)
            ])
    return clauses


def ibs_function(common_data, tasks_data=None):
    inst, slv, meas, limits, info = common_data

    results = []
    bits = decode_bits(info)
    [dim_type, bd_type] = bits[:2]
    bd_base = to_number(bits[2:8], 6)
    mask_len = to_number(bits[8:24], 16)
    bd_mask = bits[24:mask_len + 24]

    supbs_vars = inst.supbs.variables()
    backdoor = inst.get_backdoor2(bd_type, bd_base, bd_mask)
    xor_indexes = list(compress(XOR_INDEXES, backdoor._mask[:32]))
    maj_indexes = list(compress(MAJ_INDEXES, backdoor._mask[32:54]))
    bent_indexes = list(compress(BENT_INDEXES, backdoor._mask[54:70]))
    other_vars = list(compress(backdoor._list[70:], backdoor._mask[70:]))
    assumption_vars = other_vars + inst.output_set.variables()
    assumption_vars += inst.extra_set.variables() if inst.extra_set else []

    for task_data in tasks_data:
        st_timestamp = now()
        task_i, task_value = task_data

        state = RandomState(seed=task_value)
        i_values = state.randint(0, bd_base, size=len(supbs_vars))
        i_assumptions = [x if i_values[i] else -x for i, x in enumerate(supbs_vars)]
        _, _, literals = slv.solve(inst, i_assumptions)

        assumptions = []
        for lit in literals:
            if abs(lit) in assumption_vars:
                assumptions.append(lit)

        constraints = []
        for i in xor_indexes:
            constraints.extend(get_constraints(xor, *i_assumptions[i:i + 2]))
        for i in maj_indexes:
            constraints.extend(get_constraints(majority, *i_assumptions[i:i + 3]))
        for i in bent_indexes:
            constraints.extend(get_constraints(bent_4, *i_assumptions[i:i + 4]))

        kwargs = {'limits': limits, 'constraints': constraints}
        status, stats, _ = slv.solve(inst, assumptions, **kwargs)
        time, value = stats['time'], meas.get(stats)
        results.append((task_i, getpid(), value, time, status, now() - st_timestamp))

    return results


class Merged64InverseBackdoorSets(Function):
    type = 'ibs'
    slug = 'function:ibs_merged64'
    name = 'Function: Merged64 Inverse Backdoor Sets'

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
    'Merged64InverseBackdoorSets'
]
