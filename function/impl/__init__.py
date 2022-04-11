from .ibs import *
from .gad import *
from .up_gad import *
from .gad_bounded import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    UPGuessAndDetermine.slug: UPGuessAndDetermine,
    BoundedGuessAndDetermine.slug: BoundedGuessAndDetermine,
    #
    InverseBackdoorSets.slug: InverseBackdoorSets,
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine',
    'BoundedGuessAndDetermine',
    #
    'InverseBackdoorSets'
]
