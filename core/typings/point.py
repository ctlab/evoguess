from numpy import sign
from typing import Collection


class Point:
    def __init__(self, backdoor):
        self.backdoor = backdoor

    def set(self, estimation):
        return Estimated(self.backdoor, estimation)

    def value(self):
        return None

    # noinspection PyUnresolvedReferences
    def compare(self, other):
        try:
            a, b = self.value(), other.value()
            difference = int(sign(a - b))
        except (TypeError, ValueError):
            difference = 0
        return difference or len(other) - len(self)

    def __lt__(self, other):
        return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __le__(self, other):
        return self.compare(other) <= 0

    def __ge__(self, other):
        return self.compare(other) >= 0

    def __len__(self):
        return len(self.backdoor)

    # def __str__(self):
    #     return '%s by %.7g (%s samples)' % (self.backdoor, self.get(), self.get('count'))

    # todo: make backdoor cache static
    def to_dict(self, replace=None):
        if replace is not None:
            guid = replace[repr(self.backdoor)]
            return {'backdoor': guid, 'size': len(self.backdoor), **self._payload}
        else:
            return {'backdoor': repr(self.backdoor), 'size': len(self.backdoor), **self._payload}


class Estimated(Point):
    def __init__(self, backdoor, estimation):
        self.estimation = estimation
        super(Point).__init__(backdoor)

    def set(self, estimation):
        raise Exception('Estimation already set')

    def value(self):
        return self.estimation.get('value', None)


Vector = Collection[Point]

__all__ = [
    'Point',
    'Vector',
    'Estimated'
]
