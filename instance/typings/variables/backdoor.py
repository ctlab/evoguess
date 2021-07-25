from .variables import *

import warnings
from copy import copy
from itertools import compress


class Backdoor(Variables):
    slug = 'backdoor'
    name = 'Backdoor'

    def __init__(self, _list=()):
        super().__init__(sorted(set(_list)))
        self._mask = [True] * self.length
        self._variables = copy(self._list)

        assert len(self._list) > 0, 'Empty backdoor'
        assert self._list[0] >= 0, 'Backdoor contains negative numbers'
        if len(_list) != self.length:
            warnings.warn('Repeating variables in backdoor', Warning)

    def variables(self):
        return self._variables

    def __copy__(self):
        return self.get_copy(self._mask)

    def _set_mask(self, mask):
        if len(mask) > self.length:
            self._mask = mask[:self.length]
        else:
            delta = self.length - len(mask)
            self._mask = mask + [False] * delta

        self._variables = list(compress(self._list, self._mask))
        return self

    def get_mask(self):
        return copy(self._mask)

    @staticmethod
    def _from_str(string):
        return Variables._from_str(string)

    def get_copy(self, mask):
        raise NotImplementedError

    def get_bases(self):
        raise NotImplementedError

    def task_count(self):
        raise NotImplementedError

    def get_masks(self):
        raise NotImplementedError

    def get_mappers(self):
        raise NotImplementedError

    @staticmethod
    def empty(base):
        raise NotImplementedError

    @staticmethod
    def parse(string):
        raise NotImplementedError


__all__ = [
    'Backdoor'
]
