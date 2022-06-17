from typing import Union

Assumptions = list[int]
Constraints = list[list[int]]
Supplements = tuple[Assumptions, Constraints]


class Var:
    def __init__(self, base: int, name: str):
        self.base = base
        self.name = name

    @property
    def deps(self) -> list['AnyVar']:
        raise NotImplementedError

    def supplements(self, value_dict) -> Supplements:
        raise NotImplementedError

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        else:
            return self.name == other.name


AnyVar = Union[Var, int]

__all__ = [
    'Var',
    'AnyVar',
    'Assumptions',
    'Constraints',
    'Supplements'
]
