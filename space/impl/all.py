from ..abc.space import *


class All(Space):
    slug = 'space:all'
    name = 'All Space'

    def create(self, instance) -> Space:
        self.variables = instance.cnf.variables()
        return self

    def expand(self) -> Space:
        return self

    def get(self) -> BaseBackdoor:
        assert self.variables is not None, ''
        return BaseBackdoor(self.variables)

