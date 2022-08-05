from math import prod
from copy import copy
from .variables import *
from itertools import compress
from util.array import list_of


class Backdoor(Variables):
    slug = 'backdoor'
    name = 'Backdoor'

    def __init__(self, variables: List[Var]):
        super().__init__(variables)
        self._var_state = None
        self._length = len(variables)
        self._mask = list_of(1, self._length)

    def _upd_var_state(self):
        # todo: remove in island based fw
        if not self._variables:
            self._var_state = list(compress(
                parse_var_file(self._path), self._mask
            ))
        else:
            #
            self._var_state = list(compress(
                self._variables, self._mask
            ))

    def variables(self) -> List[Var]:
        if not self._var_state:
            self._upd_var_state()
        return self._var_state

    def power(self) -> int:
        return prod(self.get_var_bases())

    def get_mask(self) -> List[int]:
        return copy(self._mask)

    def _set_mask(self, mask) -> 'Backdoor':
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

    def get_copy(self, mask) -> 'Backdoor':
        # todo: remove in island based fw
        if not self._variables:
            backdoor = Backdoor.from_file(self._path)
        else:
            #
            backdoor = Backdoor(self._variables)
        return backdoor._set_mask(mask)

    def __copy__(self):
        return self.get_copy(self._mask)

    @staticmethod
    def _from(string: str, rules: VarRules = ()) -> 'Backdoor':
        variables = Variables._from(string, rules)
        return Backdoor(variables.variables())

    @staticmethod
    # todo: remove in island based fw
    def from_file(path: str) -> 'Backdoor':
        variables = Variables.from_file(path)
        backdoor = Backdoor(variables.variables())
        backdoor._variables = None
        backdoor._path = path
        return backdoor

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Backdoor'
]
