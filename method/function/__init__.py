from .impl import *
from . import measure


def get_function(name):
    return {
        'gad': GuessAndDetermine,
        'ibs': InverseBackdoorSets
    }[name]


__all__ = [
    'measure',
    'get_function'
]
__all__.extend(impl.__all__)
