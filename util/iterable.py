from copy import copy
from typing import Union, Callable, Iterable, Tuple, List, Any

Dimension = Union[int, Iterable]
Predicate = Union[Callable, Iterable]


def identity(_object: Any) -> Any:
    return _object


def concat(*iterables: Iterable) -> Iterable:
    return sum(iterables, [])


def list_of(example: Any, dimension: Dimension) -> Iterable:
    if hasattr(dimension, '__iter__'):
        return [copy(example) for _ in dimension]
    else:
        return [copy(example) for _ in range(dimension)]


def pick_by(iterable: Iterable, predicate: Predicate = identity) -> Iterable:
    if isinstance(predicate, Callable):
        return [item for item in iterable if predicate(item)]
    elif isinstance(predicate, Iterable):
        return [item for i, item in enumerate(iterable) if i in predicate]
    else:
        raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')


def omit_by(iterable: Iterable, predicate: Predicate = identity) -> Iterable:
    if isinstance(predicate, Callable):
        return [item for item in iterable if not predicate(item)]
    elif isinstance(predicate, Iterable):
        return [item for i, item in enumerate(iterable) if i not in predicate]
    else:
        raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')


def slice_by(iterable: Iterable, size: int) -> List[Iterable]:
    return [iterable[i:i + size] for i in range(0, len(iterable), size)]


def split_by(iterable: Iterable, predicate: Predicate = identity) -> Tuple[Iterable, Iterable]:
    left, right = [], []
    for i, item in enumerate(iterable):
        if isinstance(predicate, Callable):
            (left if predicate(item) else right).append(item)
        elif isinstance(predicate, Iterable):
            (left if i in predicate else right).append(item)
        else:
            raise TypeError(f'unexpected predicate type: \'{type(predicate).__name__}\'')

    return left, right


def for_each(iterable: Iterable, fn: Callable):
    for item in iterable:
        fn(item)
