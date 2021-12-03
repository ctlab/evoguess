from operator import mul
from functools import reduce

from numpy import count_nonzero as cnz
from numpy.random.mtrand import randint

from utils import array, bit_mask as bm
from structure.array.domain_backdoor import DomainBackdoor


class DomainZBackdoor(DomainBackdoor):
    type = 2

    def __str__(self):
        _format = lambda x: f'{x[0]}({array.to_bit_string(x[1])})'
        parts = list(map(_format, self.snapshot()))
        return f'[{" ".join(parts)}]({cnz(self.mask)})'

    # mask
    def get_copy(self, mask):  # ok
        backdoor = DomainZBackdoor(self.base, self.list)
        return backdoor._set_mask(mask)

    # main
    def get_bases(self):  # ok
        return [1 if self.base > cnz(m) else self.base for _, m in self.snapshot()]

    def real_task_count(self):
        return reduce(mul, super().get_bases(), 1)

    def get_masks(self):  # ok
        full_mask = (2 ** self.base - 1) << 1
        return [1 if self.base > cnz(m) else full_mask for _, m in self.snapshot()]

    def get_mappers(self):
        mapper = []
        for var, mask in self.snapshot():
            if cnz(mask) == self.base:
                mapper.append(list(range(1, self.base + 1)))
            else:
                mapper.append([0] * (cnz(mask) + 1))
        return mapper

    @staticmethod
    def parse(base, line):
        _type, line = line[0], line[1:]
        assert _type == 'z', 'It\'s not a \'z\' backdoor'
        bd = DomainBackdoor.parse(base, line)
        return DomainZBackdoor(base, bd.list)._set_mask(bd.mask)

    @staticmethod
    def empty(base):  # ok
        return DomainZBackdoor(base)


__all__ = [
    'DomainZBackdoor'
]

if __name__ == '__main__':
    bd_base = 12
    dbd = DomainZBackdoor.parse(bd_base, 'z1|* 2|101 3|5')
    masks = dbd.get_masks()
    print(dbd.task_count(), dbd.real_task_count())
    print(dbd, masks)
    print(dbd, dbd.get_mappers())
    task_dimension = randint(1, bd_base + 1, size=(10, len(dbd)))
    print(list(map(list, task_dimension)))
    task_dimension = [bm.apply_masks(values, masks) for values in task_dimension]
    print(task_dimension)
    zero_bases = [min(bd_base + 1, bd_base) for bd_base in dbd.get_bases()]
    print(dbd.snapshot())
