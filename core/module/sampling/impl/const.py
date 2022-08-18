from ..sampling import *


class Const(Sampling):
    slug = 'sampling:const'

    def __init__(self, count: int, **kwargs):
        self.count = count
        super().__init__(count, **kwargs)

    def get_count(self, offset: int, size: int, results: Results) -> int:
        return max(0, min(self.count, size) - offset)

    def summarize(self, results: Results):
        return {}

    def __info__(self):
        return {
            **super().__info__(),
            'count': self.count
        }


__all__ = [
    'Const'
]
