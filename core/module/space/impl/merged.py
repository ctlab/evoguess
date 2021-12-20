from ..space import *


class Merged(Space):
    slug = 'space:merged'
    name = 'Merged(Space)'

    def __init__(self, size, rule, *args, **kwargs):
        self.size = size
        self.rule = rule
        super().__init__(*args, *kwargs)

    def get_root(self, instance: Instance):
        pass
