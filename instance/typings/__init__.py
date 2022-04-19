from .aig import *
from .cnf import *
from .cnf_plus import *
from . import variables

types = {
    AIG.slug: AIG,
    CNF.slug: CNF,
    CNFPlus.slug: CNFPlus,
    **variables.types
}
