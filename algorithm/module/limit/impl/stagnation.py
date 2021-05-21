from ..limit import *


class Stagnation(Limit):
    key = 'stagnation'
    slug = 'limit:stagnation'
    name = 'Stagnation(Limit)'

    def __init__(self, value: int):
        super().__init__(value)


__all__ = [
    'Stagnation'
]
