from ..measure import *


class LearnedLiterals(Measure):
    key = 'learned_literals'
    name = 'Measure: Learned Literals'

    def get(self, stats: Dict[str, int]):
        return max(1, stats.get(self.key, 0))


__all__ = [
    'LearnedLiterals'
]
