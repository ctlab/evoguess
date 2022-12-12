from typing import Dict, Any

from .var import *


class Index(Var):
    slug = 'var:index'

    def __init__(self, index: int):
        self.index = index
        super().__init__(2, str(index))

    @property
    def deps(self) -> List[AnyVar]:
        return [self.index]

    def supplements(self, var_map: VarMap) -> Supplements:
        value = var_map.get(self.index, var_map[self])
        return [self.index if value else -self.index], []

    def __hash__(self):
        return self.index

    def __eq__(self, other):
        if isinstance(other, int):
            return self.index == other
        elif isinstance(other, Index):
            return self.index == other.index
        else:
            return super().__eq__(other)

    def __config__(self) -> Dict[str, Any]:
        return {
            'slug': self.slug,
            'index': self.index,
        }


__all__ = [
    'Index'
]
