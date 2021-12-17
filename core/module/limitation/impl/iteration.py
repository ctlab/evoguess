from ..limitation import *


class Iteration(Limitation):
    key = 'iteration'
    slug = 'limitation:iteration'
    name = 'Iteration(Limitation)'

    def __init__(self, value: int):
        super().__init__(value)


__all__ = [
    'Iteration'
]
