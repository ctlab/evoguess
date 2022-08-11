from ..encoding import *
from ...variables.vars import Assumptions


class AIGData:
    slug = 'encoding:aig'

    def __init__(self, lines: str = None):
        self._lines = lines

    def source(self, assumptions: Assumptions = ()):
        return ''.join([
            f'{self._lines}\n',
            *(f'{x}\n' for x in assumptions)
        ])


class AIG(Encoding):
    def get_data(self) -> AIGData:
        return AIGData(self.get_raw_data())


__all__ = [
    'AIG',
    'AIGData'
]
