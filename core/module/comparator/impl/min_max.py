from ..comparator import *

from numpy import sign


class MinValueMaxSize(Comparator):
    slug = 'comparator:min_max'
    name = 'MinValueMaxSize(Comparator)'

    def compare(self, object1, object2):
        try:
            v1, v2 = object1.value(), object2.value()
            difference = int(sign(v1 - v2))
        except (TypeError, ValueError):
            difference = 0
        return difference or len(object2) - len(object1)


__all__ = [
    'MinValueMaxSize'
]
