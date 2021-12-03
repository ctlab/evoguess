from typing import List
from time import time as now

from method import Method
from output import Output
from .limit.types import Limit
from structure.array import Backdoor
from structure.individual import Individual, Population


class Algorithm:
    name = 'Algorithm'

    def __init__(self,
                 limit: Limit,
                 method: Method,
                 output: Output,
                 *args, **kwargs
                 ):
        self.limit = limit
        self.method = method
        self.output = output

    def initialize(self, backdoor: Backdoor) -> Population:
        raise NotImplementedError

    def iteration(self, population: Population) -> Population:
        raise NotImplementedError

    def start(self, backdoor: Backdoor) -> Population:
        self.output.info(self.__str__())

        st_timestamp = now()
        self.output.log(
            'Algorithm start on %f' % st_timestamp,
            '----------------------------------------'
        )
        self.limit.set('iteration', 0)
        population = self.initialize(backdoor)
        it_time = now() - st_timestamp
        self.limit.set('time', it_time)
        self._log_iteration(0, population, it_time, it_time)

        while not self.limit.exhausted():
            it = self.limit.increase('iteration')
            self.output.debug(3, 0, f'Start iteration {it}')
            it_timestamp = now()
            population = self.iteration(population)
            it_time = now() - it_timestamp
            full_time = now() - st_timestamp
            self.limit.set('time', full_time)
            self._log_iteration(it, population, it_time, full_time)

        self.output.log('Algorithm end on %f' % now())
        return population

    def _log_iteration(self, it, population, time, full_time):
        self.output.log(
            'Iteration %d (stamp: %.2f)' % (it, full_time),
            'Individuals (%d):' % len(population),
            *['-- %s' % str(i) for i in population],
            'Time: %.2f' % time,
            '----------------------------------------'
        )

    @staticmethod
    def parse(params):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            '--------------------',
            self.method,
        ]))


__all__ = [
    'List',
    'Limit',
    'Backdoor',
    'Algorithm',
    'Individual',
    'Population'
]
