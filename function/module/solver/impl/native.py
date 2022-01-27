from ..solver import *


class Native(Solver):
    path = None
    slug = 'solver:native'
    name = 'Solver: Native'

    def solve(self, clauses, assumptions, **kwargs):
        pass

    def propagate(self, clauses, assumptions, **kwargs):
        pass


class Kissat(Native):
    path = None
    slug = 'solver:native:ks'
    name = 'Solver: Kissat'
