from typing import Collection

from util.comparable import Comparable


class Point(Comparable):
    def __init__(self, comparator, backdoor):
        self.backdoor = backdoor
        self.comparator = comparator

        self.estimation = None

    def set(self, **estimation):
        if not self.estimation:
            self.estimation = estimation
        else:
            raise Exception('Estimation already set')

    def value(self):
        return self.estimation.get('value', None)

    def compare(self, other):
        return self.comparator.compare(self, other)

    def __len__(self):
        return len(self.backdoor)


Vector = Collection[Point]

__all__ = [
    'Point',
    'Vector',
]
