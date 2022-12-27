from .const import *
from .epsilon import *
from .up_steps import *

samplings = {
    Const.slug: Const,
    Epsilon.slug: Epsilon,
    UPSteps.slug: UPSteps
}

__all__ = [
    'Const',
    'Epsilon'
]
