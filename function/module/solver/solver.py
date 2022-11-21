from typing import NamedTuple, Any, Optional

from function.module.measure import Measure
from instance.module.encoding import Encoding
from instance.module.variables.vars import Supplements


class Report(NamedTuple):
    time: float
    status: str
    value: float
    model: Optional[Any]


class SPreset:
    def __init__(self, encoding: Encoding, measure: Measure):
        self.data = encoding.get_data()
        self.measure = measure

    def solve(self, supplements: Supplements, add_model: bool = True) -> Report:
        raise NotImplementedError

    def propagate(self, supplements: Supplements, add_model: bool = True) -> Report:
        raise NotImplementedError


class Solver:
    slug = 'solver'

    def preset(self, encoding: Encoding, measure: Measure) -> SPreset:
        raise NotImplementedError

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug
        }


__all__ = [
    'Report',
    'Solver',
    'SPreset',
]
