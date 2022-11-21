from .var import *
from .var_d import *
from .var_i import *
from .var_s import *


def compress(*args: Supplements) -> Supplements:
    assumptions, constraints = [], []
    for supplements in args:
        assumptions.extend(supplements[0])
        constraints.extend(supplements[1])
    return assumptions, constraints


__all__ = [
    'Index',
    'Domain',
    'Switch',
    'XorSwitch',
    'Bent4Switch',
    'MajoritySwitch',
    # types
    'Var',
    'AnyVar',
    'VarMap',
    'Assumptions',
    'Constraints',
    'Supplements',
    # utils
    'compress'
]
