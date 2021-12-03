from .backdoor import *


class Interval:
    def __init__(self, st, length):
        self.st, self.end = st, st + length
        self.list = list(range(st, self.end))

        if self.st < 0:
            raise Exception('Interval contains negative numbers')

    def __len__(self):
        return self.end - self.st

    def __str__(self):
        return '%s..%s' % (self.st, self.end - 1)

    def __iter__(self):
        return self.list.__iter__()

    def values(self, **kwargs):
        return get_values(self.list, **kwargs)

    def to_backdoor(self, base):
        return Backdoor(base, self.list)

    def filter(self, mask):
        length = min(len(mask), self.__len__())
        return [self.list[i] for i in range(length) if mask[i]]


__all__ = [
    'Interval'
]
