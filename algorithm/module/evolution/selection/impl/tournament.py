from ..selection import *


class Tournament(Selection):
    slug = 'selection:tournament'
    name = 'Tournament(Selection)'

    def __init__(self, number_of_rounds, **kwargs):
        super().__init__(**kwargs)
        self.number_of_rounds = number_of_rounds

    def breed(self, estimated: Vector, size: int) -> Vector:
        pass

    def __info__(self):
        return {
            **super().__info__(),
            'number_of_rounds': self.number_of_rounds
        }


__all__ = [
    'Tournament'
]
