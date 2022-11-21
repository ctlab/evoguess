from .best import *
from .roulette import *
from .tournament import *

selections = {
    Best.slug: Best,
    Roulette.slug: Roulette,
    Tournament.slug: Tournament
}

__all__ = [
    'Best',
    'Roulette',
    'Tournament'
]
