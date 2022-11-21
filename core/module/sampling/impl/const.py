from ..sampling import *


class Const(Sampling):
    slug = 'sampling:const'

    def __init__(self,
                 count: int,
                 split_into: int):
        self.count = count
        super().__init__(count, split_into)

    def summarize(self, results: Results) -> Dict[str, Any]:
        return {}

    def get_count(self, offset: int, size: int, results: Results) -> int:
        return max(0, min(self.count, size) - offset)

    def __info__(self):
        return {
            **super().__info__(),
            'count': self.count
        }


__all__ = [
    'Const'
]
