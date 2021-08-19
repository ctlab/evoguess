from ..selection import *


class Tournament(Selection):
    slug = 'selection:tournament'
    name = 'Tournament(Selection)'

    def __init__(self, rounds, **kwargs):
        self.rounds = rounds
        super().__init__(**kwargs)

    def breed(self, estimated: Vector, size: int) -> Vector:
        pass

    def __info__(self):
        return {
            **super().__info__(),
            'rounds': self.rounds
        }


__all__ = [
    'Tournament'
]
