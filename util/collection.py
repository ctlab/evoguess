from .base import identity
from typing import Union, Callable, Collection

Predicate = Union[Callable, Collection]


def for_each(_collection: Collection, fn: Callable):
    for item in _collection: fn(item)


def pick_by(_collection: Collection, predicate: Predicate = identity):
    if isinstance(predicate, Callable):
        return [item for item in _collection if predicate(item)]
    elif isinstance(predicate, Collection):
        return [item for i, item in enumerate(_collection) if i in predicate]
    else:
        raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')


def omit_by(_collection: Collection, predicate: Predicate = identity):
    if isinstance(predicate, Callable):
        return [item for item in _collection if not predicate(item)]
    elif isinstance(predicate, Collection):
        return [item for i, item in enumerate(_collection) if i not in predicate]
    else:
        raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')


def split_by(_collection: Collection, predicate: Predicate = identity):
    left, right = [], []
    for i, item in enumerate(_collection):
        if isinstance(predicate, Callable):
            (left if predicate(item) else right).append(item)
        elif isinstance(predicate, Collection):
            (left if i in predicate else right).append(item)
        else:
            raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')

    return left, right
