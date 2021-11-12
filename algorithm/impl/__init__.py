from ._async import *
from .iterable import *
from . import _async, iterable

algorithms = {
    **_async.algorithms,
    **iterable.algorithms,
}

__all__ = [
    *_async.__all__,
    *iterable.__all__,
]
