from . import limit, evolution
from .tabu_search import TabuSearch


def get_algorithm(params):
    impl, kwargs = evolution.get_ea(params)
    if impl is not None:
        return impl, kwargs

    kwargs = TabuSearch.parse(params)
    if kwargs is not None:
        return TabuSearch, kwargs
    else:
        return None, {}


__all__ = [
    'limit',
    'evolution',
    'get_algorithm'
]
