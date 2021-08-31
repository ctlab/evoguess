from ..shaping import *

from util.array import slicer
from numpy.random.mtrand import RandomState


class Chunks(Shaping):
    slug = 'shaping:chunks'
    name = 'Shaping: Chunks'

    def __init__(self, chunk_rate, *args, **kwargs):
        self.chunk_rate = chunk_rate
        super().__init__()

    def get(self, size, tasks):
        chunks_count = max(1, self.chunk_rate * size)
        chunk_size = max(1, int(len(tasks) // chunks_count))
        return slicer(chunk_size, tasks)

    def __info__(self):
        return {
            **super().__info__(),
            'chunk_rate': self.chunk_rate
        }
