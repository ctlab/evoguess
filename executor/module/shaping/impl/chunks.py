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
        count = len(tasks)
        chunk_size = max(1, int(count // max(1, self.chunk_rate * size)))
        return [
            tuple((task[0], task) for task in task_chunk)
            for task_chunk in slicer(chunk_size, tasks)
        ]

    def __info__(self):
        return {
            **super().__info__(),
            'chunk_rate': self.chunk_rate
        }
