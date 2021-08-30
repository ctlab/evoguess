from ..shaping import *


class Single(Shaping):
    slug = 'shaping:single'
    name = 'Shaping: Single'

    def get(self, size, tasks):
        return [tuple((task[0], task) for task in tasks)]
