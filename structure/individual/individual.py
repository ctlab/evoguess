from typing import Iterable
from structure.array import Backdoor

from numpy import sign


class Individual:
    def __init__(self, backdoor: Backdoor):
        self._getter = None
        self.value = float('inf')
        self.backdoor = backdoor

    def set(self, value, **kwargs):
        self.value = value
        self._getter = kwargs.get
        return self

    def lazy_set(self, value, cache):
        self.value = value

        def getter(key):
            if not cache: return None
            kwargs = cache.load(str(self.backdoor))
            return kwargs and kwargs.get(key)

        self._getter = getter
        return self

    def get(self, key=None):
        if key is None:
            return self.value
        else:
            return self._getter(key)

    def compare(self, other):
        try:
            vs = int(sign(self.value - other.value))
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

    def __str__(self):
        return '%s by %.7g (%s samples)' % (self.backdoor, self.value, self.get('count'))


Population = Iterable[Individual]

__all__ = [
    'Individual',
    'Population'
]
