from ..limit import *


class Iteration(Limit):
    key = 'iteration'
    slug = 'limit:iteration'
    name = 'Iteration(Limit)'

    def __init__(self, value: int):
        super().__init__(value)


__all__ = [
    'Iteration'
]
