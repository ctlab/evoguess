import sys

from ..encoding import Encoding, EncodingData

from instance.module.variables.vars import Assumptions


class AIGData(EncodingData):
    def __init__(self, lines: str = None):
        self._lines = lines

    def source(self, assumptions: Assumptions = ()) -> str:
        return ''.join([
            f'{self._lines}\n',
            *(f'{x}\n' for x in assumptions)
        ])

    @property
    def max_literal(self) -> int:
        # todo: parse raw data
        return sys.maxint


class AIG(Encoding):
    slug = 'encoding:aig'

    def get_data(self) -> AIGData:
        return AIGData(self.get_raw_data())


__all__ = [
    'AIG',
    'AIGData'
]
