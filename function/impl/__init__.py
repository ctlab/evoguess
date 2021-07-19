from .gad import *
from .up_gad import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    UPGuessAndDetermine.slug: UPGuessAndDetermine
}

__all__ = [
    'GuessAndDetermine',
    'UPGuessAndDetermine'
]
