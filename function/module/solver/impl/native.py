from ..solver import *

import re
from os.path import join
from time import time as now
from util.array import concat
from util.const import SOLVER_PATH
from subprocess import Popen, TimeoutExpired, PIPE

STATUSES = {
    10: True,
    20: False
}


class Native(Solver):
    file = None
    budget = None
    statistic = {}
    stdin_file = None
    stdout_file = None
    slug = 'solver:native'
    name = 'Solver: Native'

    solution = re.compile(r'^v ([-\d ]*)', re.MULTILINE)

    def propagate(self, instance, assumptions, **kwargs):
        raise NotImplementedError

    def solve(self, instance, assumptions, limits=None, **kwargs):
        launch_args = [join(SOLVER_PATH, self.file)]

        clauses = instance.cnf.source(assumptions)
        if self.stdin_file is not None:
            # create input temp file
            launch_args.append(self.stdin_file % '<filepath>')

        if self.stdout_file is not None:
            # create output temp file
            launch_args.append(self.stdout_file % '<filepath>')

        timeout = limits.get('time_limit')
        for key in self.budget.keys():
            if limits and limits.get(key, 0) > 0 and self.budget[key]:
                launch_args.append(self.budget[key] % limits[key])

        timestamp = now()
        timeout = timeout and timeout + 1
        process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            output, error = process.communicate(clauses.encode(), timeout)
            statistics, solution = self.parse(output.decode())
            status = STATUSES.get(process.returncode)
        except TimeoutExpired:
            process.terminate()
            status, statistics, solution = None, {}, []

        statistics = {**statistics, 'time': now() - timestamp}
        return status, statistics, solution

    def parse(self, output):
        statistics = {}
        for key, pattern in self.statistic.items():
            result = pattern.search(output)
            statistics[key] = result and int(result.group(1))

        return statistics, concat(*[
            [int(var) for var in line.split()]
            for line in self.solution.findall(output)
        ])


class Rokk(Native):
    file = 'rokk'
    slug = 'solver:native:rokk'
    name = 'Solver: Native(ROKK)'

    stdin_file = None
    stdout_file = None
    budget = {
        'time_limit': '-cpu-lim=%d',
        'conf_budget': None,
        'prop_budget': None,
        'decs_budget': None,
    }


class Kissat(Native):
    slug = 'solver:native:kissat'
    name = 'Solver: Native(Kissat)'
    file = 'kissat-sc2021/build/kissat'

    stdin_file = None
    stdout_file = None
    budget = {
        'time_limit': '--time=%d',
        'conf_budget': '--conflicts=%d',
        'decs_budget': '--decisions=%d',
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^c clauses_learned:\s+(\d+)', re.MULTILINE),
    }


__all__ = [
    'Rokk',
    'Kissat'
]
