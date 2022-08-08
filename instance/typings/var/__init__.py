from .var import *

from .var_i import *
from .var_s import *
from .var_d import *


def compress(*args: Supplements) -> Supplements:
    assumptions, constraints = [], []
    for supplements in args:
        assumptions.extend(supplements[0])
        constraints.extend(supplements[1])
    return assumptions, constraints
