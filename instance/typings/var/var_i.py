from .var import *


class Index(Var):
    def __init__(self, index: int):
        self.index = index
        super().__init__(2, str(index))

    @property
    def deps(self) -> List[AnyVar]:
        return [self.index]

    def supplements(self, value_dict) -> Supplements:
        return [self.index if value_dict[self.index] else -self.index], []

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        if isinstance(other, int):
            return self.index == other
        else:
            return self.index == other.index


__all__ = [
    'Index'
]
