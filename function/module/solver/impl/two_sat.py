from time import time as now
from typing import Type, Dict
from pysat import solvers as pysat

from ..solver import Report
from .pysat import IncrPySAT, PySAT

from function.module.measure import Measure
from instance.module.encoding.impl.cnf import Clause
from instance.module.encoding import EncodingData, CNFData, CNFPData
from instance.module.variables.vars import Supplements, Assumptions


def is2sat(clause: Clause, value_map: Dict[int, int]) -> bool:
    count = len(clause)
    for literal in clause:
        value = value_map.get(abs(literal))
        if value is None:
            continue
        if literal == value:
            return True
        else:
            count -= 1

    return count <= 2


def check(data: EncodingData, report: Report, add_model: bool = True) -> Report:
    # todo: make report status as bool
    if report.status == 'SAT':
        return report

    time, status, value, literals = report
    if isinstance(data, CNFData) and not isinstance(data, CNFPData):
        value_map = {abs(lit): lit for lit in literals}
        stamp, model = now() - time, literals if add_model else None
        for clause in data.clauses():
            # todo: handle constraints
            if not is2sat(clause, value_map):
                return Report(now() - stamp, 'UNSAT', value, model)
        return Report(now() - stamp, 'SAT', value, model)
    else:
        raise TypeError('TwoSAT works only with CNF encodings')


class IncrTwoSAT(IncrPySAT):
    def solve(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return self.solve(assumptions, add_model)

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return check(self.data, super().propagate(assumptions, add_model), add_model)


class TwoSAT(PySAT):
    slug = 'solver:two-sat'

    def __init__(self, constructor: Type = pysat.Glucose3):
        # todo: make serializable
        super().__init__(constructor)

    def solve(self, data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        return self.propagate(data, measure, supplements)

    def propagate(self, data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        return check(data, super().propagate(data, measure, supplements), add_model)

    def use_incremental(self, data: EncodingData, measure: Measure) -> IncrTwoSAT:
        return IncrTwoSAT(self.constructor, data, measure)


__all__ = [
    'TwoSAT',
]
