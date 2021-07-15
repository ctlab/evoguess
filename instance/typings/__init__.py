from .cnf import *
from . import variables

types = {
    CNF.slug: CNF,
    **variables.types
}
