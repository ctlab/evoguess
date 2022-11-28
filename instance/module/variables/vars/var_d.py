from .var import *


class Domain(Var):
    def __init__(self, name: str, group: List[int]):
        self.group = group
        super().__init__(len(group), name)

    @property
    def deps(self) -> List[AnyVar]:
        return [self]

    def supplements(self, var_map: VarMap) -> Supplements:
        if self in var_map:
            return [var if var_map[self] == i else -var
                    for i, var in enumerate(self.group)], []
        else:
            return [var_map[i] for i in self.group], []


__all__ = [
    'Domain'
]
