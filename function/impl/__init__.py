from .gad import *
from .up_gad import *
from .incr_gad import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    UPGuessAndDetermine.slug: UPGuessAndDetermine,
    IncrGuessAndDetermine.slug: IncrGuessAndDetermine
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine'
]
