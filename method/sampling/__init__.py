from .impl import *

impls = [
    Const,
    Epsilon,
]


def get_sampling(params):
    for _impl in impls:
        kwargs = _impl.parse(params)
        if kwargs is not None:
            return _impl(**kwargs)


__all__ = [
    'get_sampling'
]
