from ..measure import *


class Conflicts(Measure):
    key = 'conflicts'
    name = 'Measure: Conflicts'

    def get(self, stats: Dict[str, int]):
        return max(1, stats.get(self.key, 0))


__all__ = [
    'Conflicts'
]
