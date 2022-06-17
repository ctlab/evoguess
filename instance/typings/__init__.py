from . import var
from .operator import *
from .cnf import AIG, CNF, CNFPlus

from .interval import *
from .backdoor import *
from .variables import *

types = {
    AIG.slug: AIG,
    CNF.slug: CNF,
    CNFPlus.slug: CNFPlus,
    Backdoor.slug: Backdoor,
    Interval.slug: Interval,
    Variables.slug: Variables
}

__all__ = [
    'var',
    'operator',
    'Interval',
    'Backdoor',
    'Variables'
]
