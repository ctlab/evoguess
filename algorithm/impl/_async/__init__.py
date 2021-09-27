from .elitism import Elitism
from .m_plus_l import MuPlusLambda

algorithms = {
    Elitism.slug: Elitism,
    MuPlusLambda.slug: MuPlusLambda
}

__all__ = [
    'Elitism',
    'MuPlusLambda'
]
