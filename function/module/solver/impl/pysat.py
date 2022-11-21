from ..solver import *
from ...measure import Budget

from typing import Type
from threading import Timer
from time import time as now
from pysat import solvers as pysat

from function.module.measure import Measure
from instance.module.encoding import Encoding, CNFData, CNFPData
from instance.module.variables.vars import Constraints, Supplements


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


class PySat(SPreset):
    def __init__(self, constructor: Type, encoding: Encoding, measure: Measure):
        self.constructor = constructor
        super().__init__(encoding, measure)

    def _create(self, constraints: Constraints = ()) -> pysat.Solver:
        if isinstance(self.data, CNFData):
            clauses = self.data.clauses(constraints)
            solver = self.constructor(clauses, True)
            if isinstance(self.data, CNFPData):
                for literals, rhs in self.data.atmosts():
                    solver.add_atmost(literals, rhs)
        else:
            raise TypeError('PySat works only with CNF or CNF+ encodings')
        return solver

    def solve(self, supplements: Supplements = ((), ()), add_model: bool = True) -> Report:
        assumptions, constraints = supplements
        with self._create(constraints) as solver:
            with PySatTimer(solver, self.measure.get_budget()) as timer:
                status = solver.solve_limited(assumptions, expect_interrupt=True)
                stats = {**solver.accum_stats(), 'time': timer.get_time()}

            value, status = self.measure.check_and_get(stats, status)
            model = solver.get_model() if add_model and status else None
            return Report(stats['time'], status, value, model)

    def propagate(self, supplements: Supplements = ((), ()), add_model: bool = True) -> Report:
        assumptions, constraints = supplements
        with self._create(constraints) as solver:
            with PySatTimer(solver, ('', None)) as timer:
                status, literals = solver.propagate(assumptions)
                time, stats = timer.get_time(), solver.accum_stats()

            value, status = self.measure.check_and_get(stats, status)
            return Report(time, status, value, literals)


class Cadical(Solver):
    slug = 'solver:pysat:cd'

    def preset(self, encoding: Encoding, measure: Measure) -> SPreset:
        return PySat(pysat.Cadical, encoding, measure)


class Glucose3(Solver):
    slug = 'solver:pysat:g3'

    def preset(self, encoding: Encoding, measure: Measure) -> SPreset:
        return PySat(pysat.Glucose3, encoding, measure)


class Glucose4(Solver):
    slug = 'solver:pysat:g4'

    def preset(self, encoding: Encoding, measure: Measure) -> SPreset:
        return PySat(pysat.Glucose4, encoding, measure)


__all__ = [
    'Cadical',
    'Glucose3',
    'Glucose4'
]
