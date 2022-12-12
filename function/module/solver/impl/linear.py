# from ..solver import *
#
# import re
# from os.path import join
# from time import time as now
# from subprocess import Popen, TimeoutExpired, PIPE
#
# from util.array import concat
# from util.const import SOLVER_PATH
# from util.collection import for_each
#
# STATUSES = {
#     10: True,
#     20: False
# }
#
#
# class Linear(Solver):
#     statistic = {}
#     slug = 'solver:linear'
#     name = 'Solver: Linear'
#     file = 'linear/propagate'
#
#     budget = {
#         'time_limit': '--time=%d',
#         'conf_budget': '--conflicts=%d',
#         'decs_budget': '--decisions=%d',
#     }
#
#     solution = re.compile(r'^v ([-\d ]*)', re.MULTILINE)
#
#     def propagate(self, encoding, assumptions, **kwargs):
#         raise NotImplementedError
#
#     def solve(self, encoding, assumptions, limits=None, **kwargs):
#         launch_args = [join(SOLVER_PATH, self.file)]
#         timeout = limits and limits.get('time_limit')
#         for key in self.budget.keys():
#             if limits and limits.get(key, 0) > 0 and self.budget[key]:
#                 launch_args.append(self.budget[key] % limits[key])
#
#         timestamp = now()
#         timeout = timeout and timeout + 1
#         process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
#         try:
#             data = encoding.source(assumptions).encode()
#             output, error = process.communicate(data, timeout)
#             statistics, solution = self.parse(output.decode())
#             status = STATUSES.get(process.returncode)
#         except TimeoutExpired:
#             process.terminate()
#             status, statistics, solution = None, {}, []
#
#         statistics = {**statistics, 'time': now() - timestamp}
#         return status, statistics, solution
#
#     def parse(self, output):
#         return {}, list(map(int, output.strip().split()))
#
#
# __all__ = [
#     'Linear'
# ]
