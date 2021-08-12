from ..shaping import *


class Single(Shaping):
    slug = 'shaping:single'
    name = 'Shaping: Single'

    def get(self, size, tasks, seed=None):
        return [tuple(enumerate(tasks))]
