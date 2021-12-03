from ..selection import *


class Tournament(Selection):
    name = 'Selection: Tournament'

    def __init__(self, number_of_rounds, **kwargs):
        super().__init__(**kwargs)
        self.number_of_rounds = number_of_rounds

    def breed(self, estimated: Population, size: int) -> Population:
        pass

    def __str__(self):
        return '%s (rounds: %d, seed: %d)' % (self.name, self.number_of_rounds, self.seed)


__all__ = [
    'Tournament'
]
