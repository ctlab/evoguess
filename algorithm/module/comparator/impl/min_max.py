from ..comparator import *


class MinValueMaxSize(Comparator):
    slug = 'comparator:min_max'
    name = 'MinValueMaxSize(Comparator)'

    def compare(self, point1, point2):
        try:
            v1, v2 = point1.value(), point2.value()
            difference = int(sign(v1 - v2))
        except (TypeError, ValueError):
            difference = 0
        return difference or len(other) - len(self)
