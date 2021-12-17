from .all import *
from .subset import *
from . import subset

spaces = {
    All.slug: All,
    **subset.subsets,
}

__all__ = [
    'All',
    *subset.__all__
]
