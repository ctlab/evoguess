from ..solver import *

import re
from os import remove
from os.path import join
from time import time as now
from tempfile import NamedTemporaryFile
from subprocess import Popen, TimeoutExpired, PIPE

from util.array import concat
from util.const import SOLVER_PATH
from util.collection import for_each

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
        files, launch_args = [], [join(SOLVER_PATH, self.file)]

        constraints = kwargs.get('constraints', [])
        source = instance.cnf.source(assumptions, constraints)
        if self.stdin_file is not None:
            with NamedTemporaryFile(delete=False) as handle:
                handle.write(source.encode())
                files.append(handle.name)
                launch_args.append(self.stdin_file % handle.name)

        if self.stdout_file is not None:
            with NamedTemporaryFile(delete=False) as handle:
                files.append(handle.name)
                launch_args.append(self.stdout_file % handle.name)

        timeout = limits and limits.get('time_limit')
        for key in self.budget.keys():
            if limits and limits.get(key, 0) > 0 and self.budget[key]:
                launch_args.extend(self.budget[key](limits[key]))

        timestamp = now()
        timeout = timeout and timeout + 1
        process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            data = None if self.stdin_file else source.encode()
            output, error = process.communicate(data, timeout)

            if self.stdout_file is not None:
                with open(files[-1], 'r+') as handle:
                    statistics, solution = self.parse(handle.read())
            else:
                statistics, solution = self.parse(output.decode())

            status = STATUSES.get(process.returncode)
        except TimeoutExpired:
            process.terminate()
            status, statistics, solution = None, {}, []
        finally:
            for_each(files, remove)

        statistics = {**statistics, 'time': now() - timestamp}
        return status, statistics, solution

    def parse(self, output):
        statistics = {}
        for key, pattern in self.statistic.items():
            result = pattern.search(output)
            statistics[key] = int(result.group(1)) if result else 0

        return statistics, concat(*[
            [int(var) for var in line.split()]
            for line in self.solution.findall(output)
        ])


class Kissat(Native):
    slug = 'solver:native:kissat'
    name = 'Solver: Native(Kissat)'
    file = 'kissat-sc2021/build/kissat'

    stdin_file = None
    stdout_file = None
    budget = {
        'time_limit': lambda d: [f'--time={int(d)}'],
        'conf_budget': lambda d: [f'--conflicts={int(d)}'],
        'decs_budget': lambda d: [f'--decisions={int(d)}'],
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^c clauses_learned:\s+(\d+)', re.MULTILINE),
    }


class Cadical5(Native):
    slug = 'solver:native:cadical'
    name = 'Solver: Native(CaDiCaL)'
    file = 'cadical-rel-1.5.0/build/cadical'

    stdin_file = None
    stdout_file = None
    budget = {
        'time_limit': lambda d: ['-t', f'{int(d)}'],
        'conf_budget': lambda d: ['-c', f'{int(d)}'],
        'decs_budget': lambda d: ['-d', f'{int(d)}'],
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^c learned_lits:\s+(\d+)', re.MULTILINE),
    }


# class Rokk(Native):
#     file = 'rokk'
#     slug = 'solver:native:rokk'
#     name = 'Solver: Native(ROKK)'
#
#     stdin_file = None
#     stdout_file = None
#     budget = {
#         'time_limit': '-cpu-lim=%d',
#         'conf_budget': None,
#         'prop_budget': None,
#         'decs_budget': None,
#     }


__all__ = [
    'Kissat',
    'Cadical5'
]
