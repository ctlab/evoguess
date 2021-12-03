from typing import Dict


class Measure:
    name = 'Measure'

    def get(self, stats: Dict[str, int]):
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Dict',
    'Measure'
]
