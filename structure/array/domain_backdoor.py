import warnings

from copy import copy
from operator import mul
from functools import reduce

from numpy import count_nonzero as cnz
from numpy.random.mtrand import randint

from utils import array, numeral_system as ns, bit_mask as bm


class DomainBackdoor:
    type = 2

    # overridden methods
    def __init__(self, base, _list=()):
        self.base = base
        self.list = sorted(set(_list))
        self.length = base * len(self.list)
        self.mask = [True] * self.length

        assert len(self.list) > 0, 'Empty backdoor'
        assert self.list[0] >= 0, 'Backdoor contains negative numbers'
        if len(_list) != len(self.list):
            warnings.warn('Repeating variables in backdoor', Warning)

    def __str__(self):
        _format = lambda x: f'{x[0]}({array.to_bit_string(x[1])})'
        parts = list(map(_format, self.snapshot()))
        return f'[{" ".join(parts)}]({cnz(self.mask)})'

    def __len__(self):
        return len(self.snapshot())

    def __copy__(self):
        return self.get_copy(self.mask)

    def __iter__(self):
        for var, _ in self.snapshot():
            yield var

    def __contains__(self, item):
        try:
            return cnz(self._chunk_mask()[self.list.index(item)])
        except ValueError:
            return False

    def __hash__(self):
        return hash(tuple(self.snapshot()))

    # mask
    def _chunk_mask(self):
        return array.chunk_slice(self.base, self.mask)

    def _set_mask(self, mask):
        if len(mask) > self.length:
            self.mask = mask[:self.length]
        else:
            delta = self.length - len(mask)
            self.mask = mask + [False] * delta
        return self

    def get_mask(self):
        return copy(self.mask)

    def get_copy(self, mask):
        backdoor = DomainBackdoor(self.base, self.list)
        return backdoor._set_mask(mask)

    def reset(self):
        return self._set_mask([True] * self.length)

    # main
    def get_bases(self):
        return [min(cnz(m) + 1, self.base) for _, m in self.snapshot()]

    def task_count(self):
        return reduce(mul, self.get_bases(), 1)

    def real_task_count(self):
        return self.task_count()

    def get_masks(self):
        return [ns.binary_to_base2(self.base, m) << 1 for _, m in self.snapshot()]

    def get_mappers(self):
        mapper = []
        for var, mask in self.snapshot():
            if cnz(mask) == self.base:
                mapper.append(list(range(1, self.base + 1)))
            else:
                var_mapper = [i + 1 for i, bit in enumerate(mask[::-1]) if bit]
                mapper.append([0] + var_mapper)
        return mapper

    def snapshot(self):
        return [(v, m) for v, m in zip(self.list, self._chunk_mask()) if cnz(m)]

    @staticmethod
    def parse(base, line):
        variables, mask = [], []
        for parted_lit in line.split(' '):
            lit, part = parted_lit.split('|')
            part = 2 ** base - 1 if part == '*' else int(part)
            if '..' in lit:
                var = lit.split('..')
                for ranged_lit in range(int(var[0]), int(var[1]) + 1):
                    variables.append(ranged_lit)
                    mask.extend(ns.base_to_binary2(base, part))
            else:
                variables.append(int(lit))
                mask.extend(ns.base_to_binary2(base, part))

        backdoor = DomainBackdoor(base, variables)
        return backdoor._set_mask(mask)

    @staticmethod
    def empty(base):
        return DomainBackdoor(base)


__all__ = [
    'DomainBackdoor'
]

if __name__ == '__main__':
    bd_base = 12
    dbd = DomainBackdoor.parse(bd_base, '1|* 2|101 3|5')
    masks = dbd.get_masks()
    print(dbd, masks)
    print(dbd, dbd.get_mappers())
    task_dimension = randint(1, bd_base + 1, size=(10, len(dbd)))
    print(list(map(list, task_dimension)))
    task_dimension = [bm.apply_masks(values, masks) for values in task_dimension]
    print(task_dimension)
    zero_bases = [min(bd_base + 1, bd_base) for bd_base in dbd.get_bases()]
    print(dbd.snapshot())
