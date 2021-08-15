from numpy import sign
from typing import Collection


class Point:
    def __init__(self, backdoor):
        super().__init__()
        self.backdoor = backdoor
        self.estimated = False
        self.estimation = {'value': float('inf')}

    def set(self, **estimation):
        if not self.estimated:
            self.estimated = True
            self.estimation = estimation
            return self
        else:
            raise Exception('Estimation already set')

    def get(self, key='value'):
        return self.estimation.get(key, None)

    def compare(self, other):
        try:
            vs = int(sign(self.get() - other.get()))
        except ValueError:
            vs = 0
        return vs or len(other) - len(self)

    def __len__(self):
        return len(self.backdoor)

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

    # def __str__(self):
    #     return '%s by %.7g (%s samples)' % (self.backdoor, self.get(), self.get('count'))

    def to_dict(self):
        return {'backdoor': repr(self.backdoor), 'size': len(self.backdoor), **self.estimation}


Vector = Collection[Point]

__all__ = [
    'Point',
    'Vector'
]
