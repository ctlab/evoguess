from ..limitation import *


class Iteration(Limitation):
    key = 'iteration'
    slug = 'limitation:iteration'

    def __init__(self, value: Numeral):
        super().__init__(value)


__all__ = [
    'Iteration'
]
