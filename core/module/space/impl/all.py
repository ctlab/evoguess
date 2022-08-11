from ..space import *


class All(Space):
    slug = 'space:all'
    name = 'All(Space)'

    def get_root(self, instance: Instance):
        return instance.encoding.variables()


__all__ = [
    'All'
]
