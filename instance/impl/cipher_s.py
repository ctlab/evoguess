from .instance import *

from util.array import concat
from numpy.random import RandomState
from ..module.variables import Variables
from function.module.solver.impl.pysat import Glucose3
from ..module.variables.vars import Assumptions, Constraints, Supplements, compress


class StreamCipher(Instance):
    slug = 'cipher:stream'

    def __init__(self, input_set: Variables, output_set: Variables, extra_set: Variables = None, **kwargs):
        self.input_set = input_set
        self.output_set = output_set
        super().__init__(**kwargs)

        self.extra_set = extra_set or Variables([])

    def _get_inversion_vars(self, *args: Variables):
        return [
            *self.extra_set.variables(),
            *self.output_set.variables(),
            *concat(*(arg.variables() for arg in args))
        ]

    def _propagate(self, assumptions: Assumptions, constraints: Constraints):
        # todo: move to solver module
        return Glucose3().solve(
            self.encoding_data(), assumptions, constraints=constraints
        )[2]

    def _get_propagation_sups(self, state: RandomState) -> Supplements:
        var_deps = self.input_set.get_var_deps()
        deps_bases = self.input_set.get_deps_bases()
        deps_values = {
            var: value for var, value in
            zip(var_deps, state.randint(0, deps_bases))
        }
        return compress(*(
            var.supplements(deps_values) for var in self.input_set
        ))

    def get_solution(self, state: RandomState):
        return self._propagate(*self._get_propagation_sups(state))

    def get_supplements(self, *args: Variables, **kwargs) -> Supplements:
        solution_values = {
            abs(lit): 1 if lit > 0 else 0 for lit in
            self.get_solution(kwargs.get('state', RandomState()))
        }
        return compress(*(
            var.supplements(solution_values)
            for var in self._get_inversion_vars(*args)
        ))

    def __info__(self):
        return {
            **super().__info__(),
            'input_set': self.input_set.__info__(),
            'extra_set': self.extra_set.__info__(),
            'output_set': self.output_set.__info__(),
        }


__all__ = [
    'StreamCipher'
]
