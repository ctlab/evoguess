from typing import Union, List, Tuple, Dict

Assumptions = List[int]
Constraints = List[List[int]]
Supplements = Tuple[Assumptions, Constraints]

AnyVar = Union['Var', int]
VarMap = Dict[AnyVar, int]


class Var:
    def __init__(self, base: int, name: str):
        self.base = base
        self.name = name

    @property
    def deps(self) -> List[AnyVar]:
        raise NotImplementedError

    def supplements(self, var_map: VarMap) -> Supplements:
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


__all__ = [
    'Var',
    # types
    'List',
    'AnyVar',
    'VarMap',
    'Assumptions',
    'Constraints',
    'Supplements'
]
