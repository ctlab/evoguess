from .elitism import *
from .m_plus_l import *

algorithms = {
    Elitism.slug: Elitism,
    MuPlusLambda.slug: MuPlusLambda
}

__all__ = [
    'algorithms',
    # impls
    'Elitism',
    'MuPlusLambda'
]
