from .elitism import Elitism
from .m_plus_l import MuPlusLambda
from .m_comma_l import MuCommaLambda

algorithms = {
    Elitism.slug: Elitism,
    MuPlusLambda.slug: MuPlusLambda,
    MuCommaLambda.slug: MuCommaLambda
}

__all__ = [
    'Elitism',
    'MuPlusLambda',
    'MuCommaLambda'
]
