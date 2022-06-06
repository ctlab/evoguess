from operator import itemgetter

from .._abc.function import *

from os import getpid
from time import time as now
from itertools import compress
from util.numeral import base_to_binary2
from numpy.random.mtrand import RandomState

# seed: 42323
BENT_INDEXES_LIST = [
    [[45, 63, 33, 2], [54, 18, 14, 21], [20, 16, 4, 62], [43, 47, 10, 6], [3, 29, 28, 17], [46, 12, 32, 61],
     [25, 44, 59, 36], [48, 52, 50, 56], [7, 5, 40, 58], [53, 1, 9, 8], [22, 60, 24, 11], [42, 13, 26, 34],
     [57, 55, 37, 30], [19, 41, 35, 39], [15, 0, 27, 49], [31, 38, 51, 23]],
    [[32, 5, 4, 62], [41, 36, 56, 58], [9, 61, 1, 13], [49, 20, 37, 50], [42, 33, 44, 47], [48, 54, 31, 12],
     [34, 23, 60, 29], [63, 53, 10, 43], [40, 27, 15, 30], [25, 18, 24, 28], [39, 46, 3, 19], [8, 45, 38, 52],
     [55, 51, 16, 26], [14, 0, 35, 59], [17, 22, 21, 2], [6, 11, 7, 57]],
    [[46, 29, 4, 45], [10, 47, 62, 11], [60, 24, 30, 9], [6, 7, 2, 27], [22, 5, 18, 57], [20, 12, 21, 48],
     [35, 25, 3, 52], [0, 61, 33, 23], [34, 50, 17, 38], [1, 19, 40, 49], [39, 54, 56, 15], [53, 13, 31, 58],
     [26, 59, 44, 37], [36, 32, 63, 14], [43, 28, 8, 16], [41, 55, 42, 51]],
    [[46, 44, 1, 22], [19, 47, 42, 17], [11, 39, 48, 58], [54, 8, 14, 13], [31, 55, 49, 21], [53, 30, 56, 15],
     [6, 33, 57, 20], [24, 61, 0, 9], [5, 51, 35, 3], [60, 16, 41, 40], [50, 43, 25, 62], [4, 29, 63, 34],
     [23, 59, 37, 26], [28, 27, 38, 7], [32, 45, 52, 10], [18, 2, 36, 12]],
    [[22, 3, 11, 5], [56, 47, 29, 43], [33, 27, 19, 32], [34, 14, 0, 59], [44, 51, 2, 26], [15, 40, 41, 38],
     [36, 46, 16, 13], [49, 23, 63, 45], [9, 60, 1, 20], [24, 31, 48, 35], [57, 18, 50, 42], [12, 61, 52, 6],
     [58, 62, 28, 53], [30, 54, 25, 21], [4, 10, 55, 39], [17, 7, 8, 37]],
    [[41, 3, 17, 49], [38, 62, 34, 42], [30, 52, 33, 19], [56, 8, 15, 0], [22, 37, 23, 29], [27, 54, 45, 5],
     [24, 50, 58, 61], [36, 26, 51, 31], [57, 18, 59, 32], [6, 39, 1, 11], [55, 21, 63, 44], [48, 47, 53, 40],
     [2, 25, 13, 46], [9, 20, 60, 43], [28, 12, 4, 10], [16, 35, 14, 7]],
    [[51, 24, 7, 0], [28, 16, 37, 12], [21, 2, 9, 56], [18, 63, 49, 57], [54, 42, 44, 43], [19, 15, 59, 41],
     [38, 39, 17, 60], [45, 55, 62, 47], [36, 34, 32, 22], [35, 1, 53, 3], [26, 33, 50, 11], [20, 52, 25, 5],
     [48, 58, 40, 4], [29, 6, 10, 23], [46, 14, 8, 13], [31, 27, 61, 30]],
    [[56, 58, 52, 2], [60, 50, 6, 26], [46, 43, 47, 59], [12, 53, 1, 9], [40, 21, 61, 18], [27, 19, 11, 36],
     [8, 49, 13, 14], [29, 57, 54, 63], [28, 15, 30, 37], [20, 51, 4, 62], [34, 39, 24, 55], [48, 31, 22, 35],
     [42, 44, 23, 7], [16, 10, 33, 5], [3, 0, 32, 17], [25, 38, 45, 41]],
    [[61, 39, 18, 55], [43, 6, 57, 52], [1, 50, 3, 51], [9, 46, 25, 10], [56, 32, 53, 0], [60, 13, 30, 45],
     [37, 54, 2, 44], [17, 21, 62, 48], [23, 7, 20, 33], [63, 42, 15, 11], [36, 40, 35, 16], [31, 34, 24, 49],
     [19, 27, 22, 47], [29, 14, 5, 12], [58, 38, 8, 4], [26, 28, 41, 59]],
    [[17, 62, 0, 18], [32, 47, 53, 16], [19, 34, 40, 5], [59, 22, 38, 28], [23, 20, 10, 27], [63, 49, 52, 15],
     [1, 58, 13, 51], [4, 37, 57, 61], [45, 33, 6, 42], [29, 14, 26, 56], [46, 2, 25, 54], [43, 8, 39, 36],
     [41, 11, 48, 30], [60, 35, 55, 9], [21, 7, 12, 24], [31, 44, 3, 50]]
]

MAJ_INDEXES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
               [24, 25, 26], [27, 28, 29], [30, 31, 32], [33, 34, 35], [36, 37, 38], [39, 40, 41], [42, 43, 44],
               [45, 46, 47], [48, 49, 50], [51, 52, 53], [54, 55, 56], [57, 58, 59], [60, 61, 62], [61, 62, 63]]
XOR_INDEXES = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19], [20, 21],
               [22, 23], [24, 25], [26, 27], [28, 29], [30, 31], [32, 33], [34, 35], [36, 37], [38, 39], [40, 41],
               [42, 43], [44, 45], [46, 47], [48, 49], [50, 51], [52, 53], [54, 55], [56, 57], [58, 59], [60, 61],
               [62, 63]]


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
    # start: 54, end: 214
    bent_indexes_list, bent_length = [], 16
    for i, st in enumerate(range(54, 214, bent_length)):
        end = st + bent_length
        bent_indexes_list.append(list(compress(BENT_INDEXES_LIST[i], backdoor._mask[st:end])))

    other_vars = list(compress(backdoor._list[214:], backdoor._mask[214:]))
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
        for xor_index in xor_indexes:
            args = [f(i_assumptions) for f in map(itemgetter, xor_index)]
            constraints.extend(get_constraints(xor, *args))
        for maj_index in maj_indexes:
            args = [f(i_assumptions) for f in map(itemgetter, maj_index)]
            constraints.extend(get_constraints(majority, *args))
        for bent_indexes in bent_indexes_list:
            for bent_index in bent_indexes:
                args = [f(i_assumptions) for f in map(itemgetter, bent_index)]
                constraints.extend(get_constraints(bent_4, *args))

        kwargs = {'limits': limits, 'constraints': constraints}
        status, stats, _ = slv.solve(inst, assumptions, **kwargs)
        time, value = stats['time'], meas.get(stats)
        results.append((task_i, getpid(), value, time, status, now() - st_timestamp))

    return results


class Merged6410InverseBackdoorSets(Function):
    type = 'ibs'
    slug = 'function:ibs_merged64_10'
    name = 'Function: Merged64 10 Inverse Backdoor Sets'

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
    'Merged6410InverseBackdoorSets'
]
