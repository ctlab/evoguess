from ..shaping import *

from util.array import slice_by_size
from numpy.random.mtrand import RandomState


class Chunks(Shaping):
    slug = 'shaping:chunks'
    name = 'Shaping: Chunks'

    def __init__(self, chunk_size, *args, **kwargs):
        self.chunk_size = chunk_size
        super().__init__(*args, **kwargs)

    def get(self, size, tasks):
        return slice_by_size(self.chunk_size, tasks)

    def __info__(self):
        return {
            **super().__info__(),
            'chunk_size': self.chunk_size
        }
