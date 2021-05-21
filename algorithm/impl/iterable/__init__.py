from .mu_plus_lambda import MuPlusLambda
from .mu_comma_lambda import MuCommaLambda

algorithms = {
    MuPlusLambda.slug: MuPlusLambda,
    MuCommaLambda.slug: MuCommaLambda
}

__all__ = [
    'MuPlusLambda',
    'MuCommaLambda'
]
