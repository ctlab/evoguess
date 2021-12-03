from ..solver import *

from pysat import solvers
from threading import Timer
from time import time as now

saved_stats = {}
saved_solvers = {}


class PySat(Solver):
    name = 'Solver'
    constructor = None

    def __init__(self, use_keys=False, incr_values=False):
        self.use_keys = use_keys
        self.incr_values = incr_values

    def solve(self, clauses, assumptions, limit=0, key=None):
        can_save = self.use_keys and (key is not None)
        if can_save and key in saved_solvers:
            from_saved = True
            solver = saved_solvers[key]
        else:
            from_saved = False
            solver = self.constructor(bootstrap_with=clauses, use_timer=True)
            if can_save:
                saved_solvers[key] = solver

        if limit > 0:
            timer = Timer(limit, solver.interrupt, ())
            timer.start()

            timestamp = now()
            status = solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
            full_time, time = now() - timestamp, solver.time()

            if timer.is_alive():
                timer.cancel()
            else:
                solver.clear_interrupt()
        else:
            timestamp = now()
            status = solver.solve(assumptions=assumptions)
            full_time, time = now() - timestamp, solver.time()

        solution = solver.get_model() if status else None
        statistics = solver.accum_stats()

        if can_save:
            if from_saved:
                new_stats = {}
                # first_stats, last_stats
                fs, ls = saved_stats[key]
                for measure in statistics.keys():
                    if self.incr_values:
                        new_stats[measure] = statistics[measure] - ls[measure]
                    else:
                        new_stats[measure] = statistics[measure] + fs[measure] - ls[measure]

                saved_stats[key] = (fs, statistics)
                statistics = new_stats
            else:
                saved_stats[key] = (statistics, statistics)

        statistics['time'] = time
        if not can_save:
            solver.delete()

        return status, statistics, solution, from_saved

    def __str__(self):
        return self.name

    @staticmethod
    def clear(max_key: int):
        cleared, errors = 0, 0
        for _key in list(saved_solvers.keys()):
            if _key <= max_key:
                try:
                    saved_solvers[_key].delete()
                    cleared += 1
                except Exception:
                    errors += 1
                finally:
                    del saved_solvers[_key]
                    if _key in saved_stats:
                        del saved_stats[_key]

        return cleared, errors


#
# ----------------------------------------------------------------
#


class Cadical(PySat):
    name = 'Solver: Cadical'
    constructor = solvers.Cadical


class Glucose3(PySat):
    name = 'Solver: Glucose3'
    constructor = solvers.Glucose3


class Glucose4(PySat):
    name = 'Solver: Glucose4'
    constructor = solvers.Glucose4


class Lingeling(PySat):
    name = 'Solver: Lingeling'
    constructor = solvers.Lingeling


class MapleChrono(PySat):
    name = 'Solver: MapleChrono'
    constructor = solvers.MapleChrono


class MapleCM(PySat):
    name = 'Solver: MapleCM'
    constructor = solvers.MapleCM


class MapleSAT(PySat):
    name = 'Solver: MapleSAT'
    constructor = solvers.Maplesat


class Minicard(PySat):
    name = 'Solver: Minicard'
    constructor = solvers.Minicard


class Minisat22(PySat):
    name = 'Solver: Minisat22'
    constructor = solvers.Minisat22


class MinisatGH(PySat):
    name = 'Solver: MinisatGH'
    constructor = solvers.MinisatGH


solvers_dict = {
    'cd': Cadical,
    'g3': Glucose3,
    'g4': Glucose4,
    'lgl': Lingeling,
    'mcb': MapleChrono,
    'mcm': MapleCM,
    'mpl': MapleSAT,
    'mc': Minicard,
    'm22': Minisat22,
    'mgh': MinisatGH,
}


def get(key, *args, **kwargs):
    return solvers_dict[key](*args, **kwargs)


__all__ = [
    'get',
    'Cadical',
    'Glucose3',
    'Glucose4',
    'Lingeling',
    'MapleChrono',
    'MapleCM',
    'Minicard',
    'Minisat22',
    'MinisatGH'
]
