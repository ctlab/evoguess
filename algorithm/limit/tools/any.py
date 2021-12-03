from ..limit import *


class Any(Limit):
    name = 'Limit: Any'

    def __init__(self, *args):
        super().__init__()
        self.args = args
        for arg in args:
            arg.limits = self.limits

    def exhausted(self) -> bool:
        return any(arg.exhausted() for arg in self.args)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            *('  ' + str(arg) for arg in self.args)
        ]))


__all__ = [
    'Any'
]
