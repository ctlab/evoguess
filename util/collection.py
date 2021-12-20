from .base import identity

from typing import Collection, Callable, Any


def for_each(_collection: Collection, fn: Callable):
    for item in _collection:
        fn(item)


def pick_by(_collection: Collection, predicate: Any = identity):
    if isinstance(predicate, Callable):
        return [item for item in _collection if predicate(item)]
    elif isinstance(predicate, Collection):
        return [item for i, item in enumerate(_collection) if i in predicate]


def omit_by(_collection: Collection, predicate: Any = identity):
    if isinstance(predicate, Callable):
        return [item for item in _collection if not predicate(item)]
    elif isinstance(predicate, Collection):
        return [item for i, item in enumerate(_collection) if i not in predicate]


def split_by(_collection: Collection, predicate: Any = identity):
    left, right = [], []
    for i, item in enumerate(_collection):
        if isinstance(predicate, Callable):
            (left if predicate(item) else right).append(item)
        elif isinstance(predicate, Collection):
            (left if i in predicate else right).append(item)

    return left, right
