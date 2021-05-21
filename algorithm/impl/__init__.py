from .iterable import *
from .streaming import *
from . import iterable, streaming

algorithms = {
    **iterable.algorithms,
    **streaming.algorithms
}

__all__ = [
    *iterable.__all__,
    *streaming.__all__
]
