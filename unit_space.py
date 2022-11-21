from numpy import argsort
from function.module.solver import pysat


class UPSubset(Space):
    slug = 'space:subset:up'

    def __init__(self, count, *args, **kwargs):
        self.count = count
        self.variables = None
        super().__init__(*args, **kwargs)

    def get_root(self, instance: Instance):
        if not self.variables:
            solver = pysat.Glucose3()
            clauses = instance.cnf.clauses()
            variables = instance.cnf.variables()

            with solver.prototype(clauses) as solver:
                variable_weights = [len({
                    *map(abs, solver.propagate([variable])[2]),
                    *map(abs, solver.propagate([-variable])[2])
                }) for variable in variables]

            indexes = argsort(variable_weights)[:self.count]
            self.variables = [variables[i] for i in indexes]

        return self.variables
