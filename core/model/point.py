from typing import List, Dict, Any

from typings.ordered import Ordered
from typings.optional import Primitive
from core.module.comparator import Comparator
from instance.module.variables import Backdoor


class Point(Ordered):
    def __init__(self, backdoor: Backdoor, comparator: Comparator):
        self.estimation = {}
        self.backdoor = backdoor
        super().__init__(comparator)

    def new(self, backdoor: Backdoor) -> 'Point':
        return Point(backdoor, self.comparator)

    def set(self, **estimation: Primitive) -> 'Point':
        if 'value' in self.estimation:
            raise Exception('Estimation already set')
        self.estimation.update(estimation)
        return self

    def __len__(self):
        return len(self.backdoor)

    def value(self) -> float:
        return self.estimation.get('value')

    def estimated(self) -> bool:
        return self.value() is not None


Vector = List[Point]

__all__ = [
    'Point',
    'Vector',
]
