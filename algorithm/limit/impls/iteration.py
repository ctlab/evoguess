from ..limit import *


class Iteration(Limit):
    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit
        self.name = 'Limit: Iteration (%d)' % limit

    def exhausted(self) -> bool:
        iteration = self.get('iteration')
        return iteration > self.limit


__all__ = [
    'Iteration'
]
