from .var import Index
from .variables import Variables

from re import search


class Interval(Variables):
    slug = 'interval'
    name = 'Interval'

    def __init__(self, start, length):
        self.end = start + length - 1
        self.start, self.length = start, length
        assert self.length > 0, "Empty interval"
        super().__init__([
            Index(i) for i in range(start, self.end + 1)
        ])

    def __str__(self):
        return f'{self.start}..{self.end}'

    @staticmethod
    def _from(string, **kwargs):
        try:
            a, b = search(r'(\d+)..(\d+)', string).groups()
            return Interval(int(a), int(b) - int(a) + 1)
        except (AttributeError, ValueError, IndexError):
            return None

    def __info__(self):
        return {
            'end': self.end,
            'start': self.start,
            'length': self.length,
        }


__all__ = [
    'Interval'
]
