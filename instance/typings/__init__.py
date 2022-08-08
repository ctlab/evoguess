from . import var
from .operator import *

from .interval import *
from .backdoor import *
from .variables import *

types = {
    Backdoor.slug: Backdoor,
    Interval.slug: Interval,
    Variables.slug: Variables
}

__all__ = [
    'var',
    'operator',
    'Interval',
    'Backdoor',
    'Variables'
]
