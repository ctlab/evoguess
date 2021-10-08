from .interval import *
from .base_backdoor import *
from .variables_list import *


types = {
    Interval.slug: Interval,
    VariablesList.slug : VariablesList
}

backdoors = {
    BaseBackdoor.slug: BaseBackdoor
}

for kind, backdoor in enumerate(backdoors.values()):
    setattr(backdoor, 'kind', kind)

__all__ = [
    'Interval',
    'BaseBackdoor',
    'VariablesList'
]
