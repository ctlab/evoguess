from . import impl
from .impl import *
from .variables import *

variables = {
    **impl.variables,
    Variables.slug: Variables,
}

__all__ = [
    'Variables',
    *impl.__all__
]
