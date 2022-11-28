from . import impl

from .impl import *
from .comparator import Comparator

impls = impl.comparators

__all__ = [
    'Comparator',
    impl.__all__
]
