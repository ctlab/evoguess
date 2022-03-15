from .ibs import *
from .gad import *
from .up_gad import *
from .gad_bounded import *
from .gad_incremental import *


functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    UPGuessAndDetermine.slug: UPGuessAndDetermine,
    IncrGuessAndDetermine.slug: IncrGuessAndDetermine,
    BoundedGuessAndDetermine.slug: BoundedGuessAndDetermine,
    #
    InverseBackdoorSets.slug: InverseBackdoorSets,
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine',
    'IncrGuessAndDetermine',
    'BoundedGuessAndDetermine',
    #
    'InverseBackdoorSets'
]
