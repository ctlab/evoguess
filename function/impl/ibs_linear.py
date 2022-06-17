# from .._abc.function import *
#
# from os import getpid
# from time import time as now
# from util.array import side_trim
# from numpy.random.mtrand import RandomState
#
#
# def ibs_function(common_data, tasks_data=None):
#     inst, slv, meas, limits, payload = common_data
#
#     results = []
#     bits = decode_bits(payload)
#     dim_type, mask = bits[0], bits[1:]
#     backdoor = inst.get_backdoor(mask=mask)
#
#     supbs_vars = inst.supbs.variables()
#     assumption_vars = backdoor.variables() + inst.output_set.variables()
#     assumption_vars += inst.extra_set.variables() if inst.extra_set else []
#
#     for task_data in tasks_data:
#         st_timestamp = now()
#         task_i, task_value = task_data
#
#         # todo: provide uniq seed
#         state = RandomState(seed=task_value)
#         i_values = state.randint(0, bd_base, size=len(supbs_vars))
#         i_assumptions = [2 * x + i_values[i] for i, x in enumerate(supbs_vars)]
#         _, _, solution = slv.solve(inst, i_assumptions)
#
#         assumptions = []
#         for lit in solution:
#             if lit // 2 in assumption_vars:
#                 assumptions.append(lit)
#
#         assert len(set(assumptions)) == len(set(assumption_vars))
#
#         status, stats, _ = slv.solve(inst, assumptions)
#         time, value = stats['time'], meas.get(stats)
#         results.append((task_i, getpid(), value, time, status, now() - st_timestamp))
#
#     return results
#
#
# class LinearInverseBackdoorSets(Function):
#     type = 'ibs'
#     slug = 'function:ibs_linear'
#     name = 'Function: Linear Inverse Backdoor Sets'
#
#     def __init__(self, *args, **kwargs):
#         self.min_p = kwargs.get('min_p', 0)
#         super().__init__(*args, **kwargs)
#
#     def get_function(self):
#         return ibs_function
#
#     def prepare_data(self, state, instance, backdoor, dim_type):
#         bd_mask = side_trim(backdoor.get_mask(), at_start=False)
#         return instance, self.solver, self.measure, {
#             self.limit_key: self.limit_value
#         }, encode_bits([*to_bits(dim_type, 1), *bd_mask])
#
#     def calculate(self, backdoor, *cases):
#         statistic = {True: 0, False: 0, None: 0}
#         process_time, time_sum, value_sum = 0, 0, 0
#
#         for case in cases:
#             time_sum += case[3]
#             value_sum += case[2]
#             process_time += case[5]
#             statistic[case[4]] += 1
#
#         value = None
#         if len(cases) > 0:
#             p = float(statistic[True]) / len(cases)
#             if p > self.min_p:
#                 value = (2 ** len(backdoor)) * 3 / p
#             else:
#                 value = float('inf')
#
#         return {
#             'time': value,
#             'value': value,
#             'count': len(cases),
#             'statistic': statistic,
#             'job_time': round(time_sum, 2),
#             'job_value': round(value_sum, 2),
#             'process_time': round(process_time, 2)
#         }
#
#
# __all__ = [
#     'LinearInverseBackdoorSets'
# ]
