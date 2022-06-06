from .ibs import *
from .gad import *
from .up_gad import *
from .ibs_linear import *
from .gad_bounded import *
from .ibs_merged64 import *
from .ibs_merged64_10 import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    UPGuessAndDetermine.slug: UPGuessAndDetermine,
    BoundedGuessAndDetermine.slug: BoundedGuessAndDetermine,
    #
    InverseBackdoorSets.slug: InverseBackdoorSets,
    LinearInverseBackdoorSets.slug: LinearInverseBackdoorSets,
    Merged64InverseBackdoorSets.slug: Merged64InverseBackdoorSets,
    Merged6410InverseBackdoorSets.slug: Merged6410InverseBackdoorSets
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine',
    'BoundedGuessAndDetermine',
    #
    'InverseBackdoorSets'
]
