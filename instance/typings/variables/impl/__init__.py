from .interval import *
from .base_backdoor import *

types = {
    Interval.slug: Interval,
}

backdoors = {
    BaseBackdoor.slug: BaseBackdoor
}

for kind, backdoor in enumerate(backdoors.values()):
    setattr(backdoor, 'kind', kind)

__all__ = [
    'Interval',
    'BaseBackdoor'
]
