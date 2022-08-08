from .cnf import *
from .cnfp import *
encodings = {
    CNF.slug: CNF,
    CNFP.slug: CNFP,
}
__all__ = [
    'CNF',
    'CNFP'
]
