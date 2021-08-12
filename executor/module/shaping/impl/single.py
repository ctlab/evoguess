from ..shaping import *


class Single(Shaping):
    slug = 'shaping:single'
    name = 'Shaping: Single'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, size, tasks, seed=None):
        return [tuple(enumerate(tasks))]
