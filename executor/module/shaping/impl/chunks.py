from ..shaping import *

from util.array import chunk_slice
from numpy.random.mtrand import RandomState


class Chunks(Shaping):
    slug = 'shaping:chunks'
    name = 'Shaping: Chunks'

    def __init__(self, chunk_rate):
        self.chunk_rate = chunk_rate
        super().__init__()

    def get(self, size, tasks, seed=None):
        rs, count = RandomState(seed=seed), len(tasks)
        chunk_size = max(1, count // (self.chunk_rate * size))
        return [
            tuple((i, tasks[i]) for i in index)
            for index in chunk_slice(chunk_size, rs.permutation(count))
        ]

    def __info__(self):
        return {
            **super().__info__(),
            'chunk_rate': self.chunk_rate
        }
