from ..shaping import *


class Single(Shaping):
    slug = 'shaping:single'
    name = 'Shaping: Single'

    def __init__(self):
        super().__init__()

    def get(self, size, tasks, seed=None):
        return [tuple((i, tasks[i]) for i in range(tasks))]
