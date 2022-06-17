from .instance import *
from ..typings import Variables
from ..typings.var import Supplements, compress

from numpy.random import RandomState


class StreamCipher(Instance):
    slug = 'cipher:stream'
    name = 'Stream Cipher'

    def __init__(self, supbs, output_set, *args, **kwargs):
        self.supbs = supbs
        self.output_set = output_set
        self.extra_set = kwargs.get('extra_set', Variables())
        super().__init__(*args, **kwargs)

    def _get_supplements(self, solver, state, intervals) -> Supplements:
        var_deps = self.supbs.get_var_deps()
        deps_bases = self.supbs.get_deps_bases()
        supbs_values = {
            var: value for var, value in
            zip(var_deps, state.randint(0, deps_bases))
        }
        assumptions, constraints = compress(*(
            var.supplements(supbs_values) for var in self.supbs
        ))
        _, _, solution = solver.solve(
            self, assumptions, constraints=constraints
        )
        solution_values = {
            abs(lit): 1 if lit else 0 for lit in solution
        }
        return compress(*(
            var.supplements(solution_values) for var in intervals
        ))

    def get_supplements(self, solver, state=None, **kwargs) -> Supplements:
        state = state if state else RandomState()
        intervals = [
            *self.extra_set.variables(),
            *self.output_set.variables(),
        ]
        if 'backdoor' in kwargs:
            intervals.extend(kwargs['backdoor'].variables())
        return self._get_supplements(solver, state, intervals)

    def __info__(self):
        return {
            **super().__info__(),
            'supbs': self.supbs.__info__(),
            'extra_set': self.extra_set.__info__(),
            'output_set': self.output_set.__info__(),
        }


__all__ = [
    'StreamCipher'
]
