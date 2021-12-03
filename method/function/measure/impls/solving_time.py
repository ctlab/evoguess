from ..measure import *


class SolvingTime(Measure):
    name = 'Measure: SolvingTime'

    def get(self, stats: Dict[str, int]):
        return stats['time']


__all__ = [
    'SolvingTime'
]
