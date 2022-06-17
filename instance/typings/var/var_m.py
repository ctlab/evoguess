from .var import *

from typing import Callable
from util.numeral import base_to_binary2


class Merged(Var):
    def __init__(self, name: str, fn: Callable, group: list):
        self.fn = fn
        self.group = group
        super().__init__(2, name)

    @property
    def deps(self) -> list[AnyVar]:
        return self.group

    def supplements(self, value_dict) -> Supplements:
        if self.name in value_dict:
            value = value_dict[self.name]
        else:
            value = self.fn(*(value_dict[i] for i in self.group))

        constraints, size = [], len(self.group)
        for case in range(0, 2 ** size):
            bits = base_to_binary2(size, case)
            if self.fn(*bits) != value:
                constraints.append([
                    -var if bit else var for
                    var, bit in zip(self.group, bits)
                ])
        return [], constraints


__all__ = [
    'Merged'
]
