from ..measure import *


class Propagations(Measure):
    key = 'propagations'
    name = 'Measure: Propagations'

    def get(self, stats: Dict[str, int]):
        return max(1, stats.get(self.key, 0))


__all__ = [
    'Propagations'
]
