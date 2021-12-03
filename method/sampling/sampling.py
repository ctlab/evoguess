from typing import Tuple
from structure.array import Backdoor


class Sampling:
    name = 'Sampling'

    def get_count(self, backdoor: Backdoor, values=()):
        raise NotImplementedError

    def get_max(self) -> int:
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Tuple',
    'Backdoor',
    'Sampling'
]
