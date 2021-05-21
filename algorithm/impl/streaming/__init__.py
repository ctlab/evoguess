from .elitism import Elitism
from .mu_plus_lambda import MuPlusLambda

algorithms = {
    Elitism.slug: Elitism,
    MuPlusLambda.slug: MuPlusLambda
}
__all__ = [
    'Elitism',
    'MuPlusLambda'
]
