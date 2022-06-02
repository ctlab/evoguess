from .ibs import *
from .gad import *
from .up_gad import *
from .ibs_linear import *
from .gad_bounded import *
from .ibs_merged64 import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    UPGuessAndDetermine.slug: UPGuessAndDetermine,
    BoundedGuessAndDetermine.slug: BoundedGuessAndDetermine,
    #
    InverseBackdoorSets.slug: InverseBackdoorSets,
    LinearInverseBackdoorSets.slug: LinearInverseBackdoorSets,
    Merged64InverseBackdoorSets.slug: Merged64InverseBackdoorSets,
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine',
    'BoundedGuessAndDetermine',
    #
    'InverseBackdoorSets'
]
