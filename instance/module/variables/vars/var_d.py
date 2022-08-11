from .var import *


class Domain(Var):
    def __init__(self, name: str, group: list):
        self.group = group
        super().__init__(len(group), name)

    @property
    def deps(self) -> VarDeps:
        return [self]

    def supplements(self, value_dict) -> Supplements:
        if self.name in value_dict:
            value = value_dict[self.name]
            return [var if value == i else -var for i, var
                    in enumerate(self.group)], []
        else:
            return [value_dict[i] for i in self.group], []


__all__ = [
    'Domain'
]
