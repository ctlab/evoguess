from time import time as now
from typing import Type, Dict
from pysat import solvers as pysat

from ..solver import Report
from .pysat import IncrPySAT, PySAT

from function.models import Status
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


def check(data: EncodingData, threshold: float, report: Report, add_model: bool = True) -> Report:
    if not isinstance(data, CNFData) or isinstance(data, CNFPData):
        raise TypeError('TwoSAT works only with CNF encodings')
    if report.status == Status.RESOLVED:
        return report

    time, value, status, literals = report
    clauses, false_count = data.clauses(), 0
    false_limit = (1 - threshold) * len(clauses)
    value_map = {abs(lit): lit for lit in literals}
    stamp, model = now() - time, literals if add_model else None
    for clause in data.clauses():  # todo: constraints not supported
        false_count += not is2sat(clause, value_map)
        if false_count > false_limit:
            return Report(now() - stamp, value, Status.SOLVED, model)
    return Report(now() - stamp, value, Status.RESOLVED, model)


class IncrTwoSAT(IncrPySAT):
    def __init__(self, threshold: float, constructor: Type, data: EncodingData, measure: Measure):
        super().__init__(constructor, data, measure)
        self.threshold = threshold

    def solve(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        # todo: maybe raise Exception?
        return self.propagate(assumptions, add_model)

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return check(self.data, self.threshold, super().propagate(assumptions), add_model)


class TwoSAT(PySAT):
    slug = 'solver:two-sat'

    def __init__(self, threshold: float = 1.0):
        super().__init__(pysat.Glucose3)
        self.threshold = threshold

    def solve(self, data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        return self.propagate(data, measure, supplements)

    def propagate(self, data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        return check(data, self.threshold, super().propagate(data, measure, supplements), add_model)

    def use_incremental(self, data: EncodingData, measure: Measure) -> IncrTwoSAT:
        return IncrTwoSAT(self.threshold, self.constructor, data, measure)


__all__ = [
    'TwoSAT',
]
