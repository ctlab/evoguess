from .var import *

from typing import Callable
from util.iterable import to_bin


class Switch(Var):
    def __init__(self, name: str, group: List[int], fn: Callable):
        self.fn = fn
        self.group = group
        super().__init__(2, name)

    @property
    def deps(self) -> List[AnyVar]:
        return self.group

    def supplements(self, var_map: VarMap) -> Supplements:
        constraints, size = [], len(self.group)
        value = var_map[self] if self in var_map else \
            self.fn(*(var_map[i] for i in self.group))
        for number in range(0, 2 ** size):
            bits = to_bin(number, size)
            if self.fn(*bits) != value:
                constraints.append([
                    -var if bit else var for
                    var, bit in zip(self.group, bits)
                ])
        return [], constraints


def xor(*args):
    return sum(args) % 2 == 1


class XorSwitch(Switch):
    def __init__(self, name: str, group: List[int]):
        super().__init__(name, group, xor)


def bent4(x1, x2, x3, x4):
    return xor(x1 and x3, x2 and x4)


class Bent4Switch(Switch):
    def __init__(self, name: str, group: List[int]):
        super().__init__(name, group, bent4)


def majority(*args):
    return sum(args) > len(args) // 2


class MajoritySwitch(Switch):
    def __init__(self, name: str, group: List[int]):
        super().__init__(name, group, majority)


__all__ = [
    'Switch',
    'XorSwitch',
    'Bent4Switch',
    'MajoritySwitch'
]
