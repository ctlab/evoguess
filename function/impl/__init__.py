from .gad import *
from .ibs import *
from .up_gad import *
from .incr_gad import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    InverseBackdoorSets.slug: InverseBackdoorSets,
    UPGuessAndDetermine.slug: UPGuessAndDetermine,
    IncrGuessAndDetermine.slug: IncrGuessAndDetermine
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine'
]
