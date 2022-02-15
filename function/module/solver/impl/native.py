from pydash import now

from ..solver import *

from os.path import join
from util.const import SOLVER_PATH
from subprocess import Popen, TimeoutExpired, PIPE


class Native(Solver):
    file = None
    budget = None
    stdin_file = None
    stdout_file = None
    slug = 'solver:native'
    name = 'Solver: Native'

    def propagate(self, clauses, assumptions, **kwargs):
        raise NotImplementedError

    def solve(self, clauses, assumptions, limits=None, **kwargs):
        launch_args = [join(SOLVER_PATH, self.file)]

        if self.stdin_file is not None:
            # create input temp file
            launch_args.append(self.stdin_file % '<filepath>')

        if self.stdout_file is not None:
            # create output temp file
            launch_args.append(self.stdout_file % '<filepath>')

        for key in self.budget.keys():
            if limits and limits.get(key, 0) > 0 and self.budget['time']:
                launch_args.append(self.budget[key] % limits[key])

        timestamp = now()
        process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            output, error = process.communicate(timeout=limits.get('time_limit'))
            status, statistics, solution = self.parse(output)
        except TimeoutExpired:
            process.kill()
            status, statistics, solution = None, {}, []

        statistics = {**statistics, 'time': now() - timestamp}
        return status, statistics, solution

    def parse_output(self):
        raise NotImplementedError


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
    }

    def parse_output(self):
        pass


class Kissat(Native):
    file = 'kissat'
    slug = 'solver:native:kissat'
    name = 'Solver: Native(Kissat)'

    stdin_file = None
    stdout_file = None
    budget = {
        'time_limit': None,
        'conf_budget': None,
        'prop_budget': None,
    }

    def parse_output(self):
        pass


__all__ = [
    'Rokk',
    'Kissat'
]
