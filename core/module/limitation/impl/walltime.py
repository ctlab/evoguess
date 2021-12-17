from ..limitation import *


class WallTime(Limitation):
    key = 'time'
    slug = 'limitation:time'
    name = 'WallTime(Limitation)'
    time_scale = [1, 60, 60, 24]

    def __init__(self, value: str):
        self.hlimit = value
        super().__init__(self._parse(value))

    def _parse(self, s):
        time_units = s.split(':')[::-1]
        time_units = time_units[:len(self.time_scale)]

        time, acc = 0, 1
        for i in range(len(time_units)):
            acc *= self.time_scale[i]
            time += int(time_units[i]) * acc

        return time

    def __info__(self):
        return {
            **super().__info__(),
            'hlimit': self.hlimit
        }


__all__ = [
    'WallTime'
]
