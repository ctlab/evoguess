from ..variables import Variables


class Interval(Variables):
    slug = 'interval'
    name = 'Interval'

    def __init__(self, start, length):
        self.start, self.end = start, start + length
        super().__init__(list(range(self.start, self.end)))

        if self.start < 0:
            raise Exception('Interval contains negative numbers')

    def __str__(self):
        return f"[{self.start}..{self.end - 1}]({self.length})"

    def __copy__(self):
        return Interval(self.start, self.length)

    def variables(self):
        return self._list

    def __info__(self):
        return {
            **super().__info__(),
            'end': self.end,
            'start': self.start,
            'length': self.length,
        }


__all__ = [
    'Interval'
]
