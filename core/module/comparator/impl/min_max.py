from ..comparator import *

from numpy import sign


class MinValueMaxSize(Comparator):
    slug = 'comparator:min_max'
    name = 'MinValueMaxSize(Comparator)'

    def compare(self, obj1, obj2):
        try:
            v1, v2 = obj1.value(), obj2.value()
            difference = int(sign(v1 - v2))
        except (TypeError, ValueError):
            difference = 0
        return difference or len(obj2) - len(obj1)


__all__ = [
    'MinValueMaxSize'
]
