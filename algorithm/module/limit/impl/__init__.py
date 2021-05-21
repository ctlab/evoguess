from .walltime import *
from .iteration import *
from .stagnation import *

limits = {
    WallTime.slug: WallTime,
    Iteration.slug: Iteration,
    Stagnation.slug: Stagnation
}

__all__ = [
    'WallTime',
    'Iteration',
    'Stagnation'
]
