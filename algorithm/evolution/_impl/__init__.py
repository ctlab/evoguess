from .elitism import *
from .mu_plus_lambda import *
from .mu_comma_lambda import *

impls = [
    Elitism,
    MuPlusLambda,
    MuCommaLambda
]


def get_ea(params):
    for impl in impls:
        kwargs = impl.parse(params)
        if kwargs is not None:
            return impl, kwargs

    return None, {}


__all__ = [
    'get_ea',
    'Elitism',
    'MuPlusLambda',
    'MuCommaLambda'
]
