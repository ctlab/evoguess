from .input_set import *
from .search_set import *

spaces = {
    InputSet.slug: InputSet,
    SearchSet.slug: SearchSet,
}

__all__ = [
    'InputSet',
    'SearchSet',
]
