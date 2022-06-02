from ..solver import *

from pysat import solvers
from threading import Timer
from time import time as now


class PySat(Solver):
    constructor = None
    slug = 'solver:pysat'
    name = 'Solver: PySat'

    def prototype(self, instance, **kwargs):
        clauses = instance.clauses(kwargs.get('constraints', []))
        solver = self.constructor(clauses, use_timer=True)
        for [literals, rhs] in kwargs.get('atmosts', []):
            solver.add_atmost(literals, rhs)
        return _IPySat(solver)

    def propagate(self, instance, assumptions, **kwargs):
        clauses = instance.clauses(kwargs.get('constraints', []))
        with self.constructor(clauses, use_timer=True) as solver:
            for [literals, rhs] in kwargs.get('atmosts', []):
                solver.add_atmost(literals, rhs)
            status, statistics, literals = self.propagate_with(solver, assumptions, **kwargs)

        return status, statistics, literals

    def solve(self, instance, assumptions, limits=None, **kwargs):
        clauses = instance.clauses(kwargs.get('constraints', []))
        with self.constructor(clauses, use_timer=True) as solver:
            for [literals, rhs] in kwargs.get('atmosts', []):
                solver.add_atmost(literals, rhs)

            if limits and limits.get('conf_budget', 0) > 0:
                kwargs['expect_interrupt'] = True
                solver.conf_budget(limits['conf_budget'])
            if limits and limits.get('prop_budget', 0) > 0:
                kwargs['expect_interrupt'] = True
                solver.prop_budget(limits['prop_budget'])
            status, statistics, solution = self.solve_with(solver, assumptions, limits, **kwargs)

        return status, statistics, solution

    @staticmethod
    def propagate_with(solver, assumptions, **kwargs):
        timestamp = now()
        status, literals = solver.propagate(assumptions=assumptions)
        full_time, time = now() - timestamp, solver.time()

        statistics = {**solver.accum_stats(), 'time': time}
        return status, statistics, literals

    @staticmethod
    def solve_with(solver, assumptions, limits, expect_interrupt=False, **kwargs):
        if limits and limits.get('time_limit', 0) > 0:
            timer = Timer(limits['time_limit'], solver.interrupt, ())
            timer.start()

            timestamp = now()
            status = solver.solve_limited(assumptions, expect_interrupt=True)
            time = now() - timestamp

            if timer.is_alive():
                timer.cancel()
            del timer
        else:
            timestamp = now()
            if not expect_interrupt:
                status = solver.solve(assumptions)
            else:
                status = solver.solve_limited(assumptions, True)
            time = now() - timestamp

        if status is None:
            solver.clear_interrupt()

        solution = solver.get_model() if status else None
        statistics = {**solver.accum_stats(), 'time': time}
        return status, statistics, solution


class _IPySat:
    def __init__(self, solver):
        self.stat = {}
        self.solver = solver

    def __enter__(self):
        return self

    def _fix_stat(self, stat):
        for key, value in stat.items():
            if key != 'time':
                stat[key] -= self.stat.get(key, 0)
                self.stat[key] = value
        return stat

    def solve(self, assumptions, limit=0, **kwargs):
        st, stat, sol = PySat.solve_with(self.solver, assumptions, limit, **kwargs)
        return st, self._fix_stat(stat), sol

    def propagate(self, assumptions, **kwargs):
        st, stat, liters = PySat.propagate_with(self.solver, assumptions, **kwargs)
        return st, self._fix_stat(stat), liters

    def __exit__(self, exc_type, exc_value, traceback):
        if self.solver:
            self.solver.delete()
            self.solver = None


#
# ----------------------------------------------------------------
#


class Cadical(PySat):
    slug = 'solver:pysat:cd'
    name = 'Solver: Cadical'
    constructor = solvers.Cadical


class Glucose3(PySat):
    slug = 'solver:pysat:g3'
    name = 'Solver: Glucose3'
    constructor = solvers.Glucose3


class Glucose4(PySat):
    slug = 'solver:pysat:g4'
    name = 'Solver: Glucose4'
    constructor = solvers.Glucose4


class Lingeling(PySat):
    slug = 'solver:pysat:lgl'
    name = 'Solver: Lingeling'
    constructor = solvers.Lingeling


class MapleChrono(PySat):
    slug = 'solver:pysat:mcb'
    name = 'Solver: MapleChrono'
    constructor = solvers.MapleChrono


class MapleCM(PySat):
    slug = 'solver:pysat:mcm'
    name = 'Solver: MapleCM'
    constructor = solvers.MapleCM


class MapleSAT(PySat):
    slug = 'solver:pysat:mpl'
    name = 'Solver: MapleSAT'
    constructor = solvers.Maplesat


class Minicard(PySat):
    slug = 'solver:pysat:mc'
    name = 'Solver: Minicard'
    constructor = solvers.Minicard


class Minisat22(PySat):
    slug = 'solver:pysat:m22'
    name = 'Solver: Minisat22'
    constructor = solvers.Minisat22


class MinisatGH(PySat):
    slug = 'solver:pysat:mgh'
    name = 'Solver: MinisatGH'
    constructor = solvers.MinisatGH


__all__ = [
    'Cadical',
    'Glucose3',
    'Glucose4',
    'Lingeling',
    'MapleChrono',
    'MapleCM',
    'MapleSAT',
    'Minicard',
    'Minisat22',
    'MinisatGH'
]
