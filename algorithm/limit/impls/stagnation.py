from ..limit import *


class Stagnation(Limit):
    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit
        self.name = 'Limit: Stagnation (%d)' % limit

    def exhausted(self) -> bool:
        stagnation = self.get('stagnation')
        return stagnation > self.limit


__all__ = [
    'Stagnation'
]
