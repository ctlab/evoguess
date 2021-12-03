from ..sampling import *

import re
from math import log, sqrt, floor


class Epsilon(Sampling):
    def __init__(self, mn, mx, step, eps, delta=0.05):
        self.delta = delta
        self.min, self.max = mn, mx
        self.step, self.eps = step, eps
        self.name = 'Sampling: Epsilon (%d..%d, eps: %.2f, delta: %.2f)' % (mn, mx, eps, delta)

    def _n_e_d(self, values):
        n = len(values)
        e = sum(values) / n
        d = sum([(value - e) ** 2 for value in values]) / (n - 1)
        return n, e, d

    def _get_eps(self, values):
        n, e, d = self._n_e_d(values)
        return sqrt(d / (self.delta * n)) / e

    def get_count(self, backdoor: Backdoor, values=()):
        count = len(values)
        bd_count = backdoor.task_count()
        if count == 0:
            return min(self.min, bd_count)
        elif count < bd_count and count < self.max:
            if self._get_eps(values) > self.eps:
                bound = min(count + self.step, self.max, bd_count)
                return bound - count
        return 0

    def get_max(self) -> int:
        return self.max

    @staticmethod
    def parse(params):
        args = re.findall(r'^(\d+):(\d+):(\d+)@((?:[0-9]*[.])?[0-9]+)(?:d((?:[0-9]*[.])?[0-9]+))?$', params)
        if len(args) > 0:
            kwargs = {
                'mn': int(args[0][0]),
                'mx': int(args[0][1]),
                'step': int(args[0][2]),
                'eps': float(args[0][3]),
            }
            if len(args[0][4]) > 0:
                kwargs['delta'] = float(args[0][4])
            return kwargs


__all__ = [
    'Epsilon'
]
