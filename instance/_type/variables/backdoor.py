from .variables import *

import warnings
from copy import copy


class Backdoor(Variables):
    slug = 'backdoor'
    name = 'Backdoor'

    def __init__(self, _list=()):
        super().__init__(sorted(set(_list)))
        self.mask = [True] * self.length

        assert len(self.list) > 0, 'Empty backdoor'
        assert self.list[0] >= 0, 'Backdoor contains negative numbers'
        if len(_list) != self.length:
            warnings.warn('Repeating variables in backdoor', Warning)

    def __copy__(self):
        return self.get_copy(self.mask)

    def _set_mask(self, mask):
        if len(mask) > self.length:
            self.mask = mask[:self.length]
        else:
            delta = self.length - len(mask)
            self.mask = mask + [False] * delta
        return self

    def get_mask(self):
        return copy(self.mask)

    def snapshot(self):
        raise NotImplementedError

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


__all__ = [
    'Backdoor'
]
