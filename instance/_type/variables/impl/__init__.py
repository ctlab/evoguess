from .interval import *
from .base_backdoor import *

types = {
    Interval.slug: Interval,
}

backdoors = {
    BaseBackdoor.slug: BaseBackdoor
}

__all__ = [
    'Interval',
    'BaseBackdoor'
]
