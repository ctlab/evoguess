from ..sampling import *


class Const(Sampling):
    slug = 'sampling:const'

    def __init__(self,
                 value: int,
                 split_into: int):
        self.value = value
        super().__init__(value, split_into)

    def summarize(self, results: Results) -> Dict[str, Any]:
        return {}

    def get_count(self, offset: int, size: int, results: Results) -> int:
        return max(0, min(self.value, size) - offset)

    def __info__(self):
        return {
            **super().__info__(),
            'value': self.value,
            'split_into': self.split_into
        }


__all__ = [
    'Const'
]
