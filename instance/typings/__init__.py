from .cnf import *
from .cnf_plus import *
from . import variables

types = {
    CNF.slug: CNF,
    CNFPlus.slug: CNFPlus,
    **variables.types
}
