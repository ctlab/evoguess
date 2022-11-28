from .indexes import Indexes
from ..var_tools import parse_range


class Interval(Indexes):
    slug = 'variables:interval'

    def __init__(self, start: int = None, length: int = None, from_string: str = None):
        if from_string:
            self.start, self.end = parse_range(from_string)
            self.from_string, self.length = from_string, None
        else:
            self.start, self.length = start, length
            self.from_string, self.end = None, start + length - 1
        super().__init__(from_iterable=range(self.start, self.end + 1))

    def __str__(self):
        return f'{self.start}..{self.end}'

    def __info__(self):
        return {
            'slug': self.slug,
            'start': self.start,
            'length': self.length,
            'from_string': self.from_string,
        }


__all__ = [
    'Interval'
]
