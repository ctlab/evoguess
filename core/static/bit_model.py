from numpy import ndarray
from numpy.random import RandomState

from function.typings import TaskId

CHUNK_LENGTH, CHUNK_SHIFT = 10, 22
DATA_MASK = (1 << CHUNK_SHIFT) - 1
CHUNK_MASK = (1 << CHUNK_LENGTH) - 1 << CHUNK_SHIFT


# todo: convert more optimal
def decimal_to_base(number, bases):
    values = []
    for base in bases[::-1]:
        number, value = divmod(number, base)
        values.insert(0, value)
    return values


class BitModel:
    def get_input(self, seed, length: int) -> list[int]:
        return list(RandomState(seed).randint(0, bd_base, length))
        # todo: apply backdoor.get_masks() to values

    def get_assumption(self, tid: TaskId, length: int) -> list[int]:
        chunk = (tid & CHUNK_MASK) >> CHUNK_SHIFT
        if not chunk:
            bases = [bd_base] * length
            values = decimal_to_base(tid & DATA_MASK, bases)
            # todo: map values using backdoor.get_mappers()
        else:
            state = RandomState(seed=tid & DATA_MASK)
            values = state.randint(0, bd_base, size=length)
            # todo: apply backdoor.get_masks() to values

        return values


BIT_MODEL = BitModel()

__all__ = [
    'BIT_MODEL',
]
