from .._abc.preprocess import Preprocess

from numpy import argsort
from function.module.solver import pysat


class PropagationSubset(Preprocess):
    slug = 'preprocess:up_subset'
    name = 'Preprocess: Propagation Subset'

    def __init__(self, top, *args, **kwargs):
        self.top = top
        self.sorted_indexes = []
        super().__init__(*args, **kwargs)

    def run(self):
        cnf = self._get('instance.cnf')
        solver = self.algorithm.method.function.solver
        solver = solver if solver.can_propagate else pysat.Glucose3()

        with solver.prototype(cnf.clauses()) as solver:
            variable_weights = [len({
                *map(abs, solver.propagate([variable])[2]),
                *map(abs, solver.propagate([-variable])[2])
            }) for variable in range(1, cnf.max_literal() + 1)]

            self.sorted_indexes = argsort(variable_weights)

        return {}


__all__ = [
    'PropagationSubset'
]
