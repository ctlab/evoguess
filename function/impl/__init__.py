from .gad import *
from .sgad import *

functions = {
    GuessAndDetermine.slug: GuessAndDetermine,
    SharedGuessAndDetermine.slug: SharedGuessAndDetermine,
}

__all__ = [
    'GuessAndDetermine',
    'SharedGuessAndDetermine'
]
