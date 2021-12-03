from ..sampling import *

import re
from math import log, floor


class Const(Sampling):
    def __init__(self, count: int):
        self.count = count
        self.name = 'Sampling: Const (%s)' % count

    def get_count(self, backdoor: Backdoor, values=()):
        count = min(self.count, backdoor.task_count())
        return max(0, count - len(values))

    def get_max(self) -> int:
        return self.count

    @staticmethod
    def parse(params):
        args = re.findall(r'^(\d+)$', params)
        return {
            'count': int(args[0])
        } if len(args) else None


__all__ = [
    'Const'
]
