from typing import Type
from threading import Timer
from time import time as now
from pysat import solvers as pysat

from ..solver import Report, Solver, IncrSolver

from function.module.measure import Measure, Budget, EMPTY_BUDGET
from instance.module.encoding import EncodingData, CNFData, CNFPData
from instance.module.variables.vars import Assumptions, Constraints, Supplements


class PySatTimer:
    def __init__(self, solver: pysat.Solver, budget: Budget):
        self._timer = None
        self._solver = solver
        self._timestamp = None
        self.key, self.value = budget

    def get_time(self) -> float:
        return now() - self._timestamp

    def interrupt(self):
        self._solver and self._solver.interrupt()

    def __enter__(self):
        if self.value is not None:
            if self.key == 'time':
                self._timer = Timer(self.value, self.interrupt, ())
                self._timer.start()
            elif self.key == 'conflicts':
                self._solver.conf_budget(int(self.value))
            elif self.key == 'propagations':
                self._solver.prop_budget(int(self.value))

        self._timestamp = now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._timer is not None:
            if self._timer.is_alive():
                self._timer.cancel()
            self._timer = None
        self._solver = None


def init(constructor: Type, data: EncodingData,
         constraints: Constraints = ()) -> pysat.Solver:
    if isinstance(data, CNFData):
        clauses = data.clauses(constraints)
        solver = constructor(clauses, True)
        if isinstance(data, CNFPData):
            for literals, rhs in data.atmosts():
                solver.add_atmost(literals, rhs)
    else:
        raise TypeError('PySat works only with CNF or CNF+ encodings')
    return solver


def solve(solver: pysat.Solver, measure: Measure,
          assumptions: Assumptions = (), add_model: bool = True) -> Report:
    with PySatTimer(solver, measure.get_budget()) as timer:
        status = solver.solve_limited(assumptions, expect_interrupt=True)
        stats = {**solver.accum_stats(), 'time': timer.get_time()}

    value, status = measure.check_and_get(stats, status)
    model = solver.get_model() if add_model and status else None
    return Report(stats['time'], status, value, model)


def propagate(solver: pysat.Solver, measure: Measure, max_literal: int,
              assumptions: Assumptions = (), add_model: bool = True) -> Report:
    with PySatTimer(solver, EMPTY_BUDGET) as timer:
        status, literals = solver.propagate(assumptions)
        stats = {**solver.accum_stats(), 'time': timer.get_time()}

    status = not (status and len(literals) < max_literal)
    value, status = measure.check_and_get(stats, status)
    return Report(stats['time'], status, value, literals if add_model else None)


class IncrPySAT(IncrSolver):
    solver = None
    last_fixed_value = None

    def __init__(self, constructor: Type, data: EncodingData, measure: Measure):
        # todo: add constraints to constructor
        self.constructor = constructor
        super().__init__(data, measure)

    def _fix(self, report: Report) -> Report:
        if self.measure.key == 'time':
            return report

        value = report.value - self.last_fixed_value
        self.last_fixed_value = report.value
        return Report(report.time, report.status, value, report.model)

    def __enter__(self):
        self.solver = init(self.constructor, self.data)
        self.last_fixed_value = 0
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.solver:
            self.solver.delete()
            self.solver = None

    def solve(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return self._fix(solve(self.solver, self.measure, assumptions, add_model))

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return self._fix(
            propagate(self.solver, self.measure, self.data.max_literal, assumptions, add_model))


class PySAT(Solver):
    def __init__(self, constructor: Type):
        self.constructor = constructor

    def solve(self, data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        assumptions, constraints = supplements
        with init(self.constructor, data, constraints) as solver:
            return solve(solver, measure, assumptions, add_model)

    def propagate(self, data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        assumptions, constraints = supplements
        with init(self.constructor, data, constraints) as solver:
            return propagate(solver, measure, data.max_literal, assumptions, add_model)

    def use_incremental(self, data: EncodingData, measure: Measure) -> IncrPySAT:
        return IncrPySAT(self.constructor, data, measure)


class Cadical(PySAT):
    slug = 'solver:pysat:cd'

    def __init__(self):
        super().__init__(pysat.Cadical)


class Glucose3(PySAT):
    slug = 'solver:pysat:g3'

    def __init__(self):
        super().__init__(pysat.Glucose3)


class Glucose4(PySAT):
    slug = 'solver:pysat:g4'

    def __init__(self):
        super().__init__(pysat.Glucose4)


__all__ = [
    'Cadical',
    'Glucose3',
    'Glucose4',
    # types
    'PySAT',
    'IncrPySAT'
]
