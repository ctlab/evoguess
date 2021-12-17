from ..space import *


class All(Space):
    slug = 'space:all'
    name = 'All(Space)'

    def get(self, instance: Instance) -> [int]:
        return instance.cnf.variables()


__all__ = [
    'All'
]
