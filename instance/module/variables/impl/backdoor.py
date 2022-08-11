from typing import Union

from ..variables import *

from math import prod
from copy import copy
from itertools import compress
from util.array import list_of

Mask = List[int]


class Backdoor(Variables):
    slug = 'variables:backdoor'

    def __init__(self, from_vars: List[Var] = None, from_file: str = None):
        super().__init__(from_vars=from_vars, from_file=from_file)
        self._length = len(super().variables())
        self._mask = list_of(1, self._length)

        self._var_state = None

    def _upd_var_state(self):
        _variables = super().variables()
        self._var_state = list(compress(
            _variables, self._mask
        ))

    def variables(self) -> List[Var]:
        if not self._var_state:
            self._upd_var_state()
        return self._var_state

    def power(self) -> int:
        return prod(self.get_var_bases())

    def get_mask(self) -> List[int]:
        return copy(self._mask)

    def _set_mask(self, mask: Mask) -> 'Backdoor':
        if len(mask) > self._length:
            self._mask = mask[:self._length]
        else:
            dl = self._length - len(mask)
            self._mask = mask + list_of(0, dl)

        self._var_deps = None
        self._var_state = None
        self._var_bases = None
        self._deps_bases = None
        return self

    def get_copy(self, mask: Mask) -> 'Backdoor':
        return Backdoor(
            from_file=self.filepath,
            from_vars=self._variables,
        )._set_mask(mask)

    def __copy__(self):
        return self.get_copy(self._mask)


__all__ = [
    'Mask',
    'Backdoor'
]
