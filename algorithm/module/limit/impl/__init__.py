from .walltime import *
from .iteration import *

limits = {
    WallTime.slug: WallTime,
    Iteration.slug: Iteration,
}

__all__ = [
    'WallTime',
    'Iteration',
]
