from ..limit import *


class WallTime(Limit):
    time_scale = [1, 60, 60, 24]

    def __init__(self, limit: str):
        super().__init__()
        self.limit = self._parse(limit)
        self.name = 'Limit: WallTime (%s)' % limit

    def exhausted(self) -> bool:
        time = self.get('time')
        return time > self.limit

    def _parse(self, s):
        time_units = s.split(':')[::-1]
        time_units = time_units[:len(self.time_scale)]

        time, acc = 0, 1
        for i in range(len(time_units)):
            acc *= self.time_scale[i]
            time += int(time_units[i]) * acc

        return time


__all__ = [
    'WallTime'
]
