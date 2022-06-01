from ..sampling import *


class Const(Sampling):
    slug = 'sampling:const'
    name = 'Sampling: Const'

    def __init__(self, count: int, *args, **kwargs):
        self.count = count
        super().__init__(count, *args, **kwargs)

    def get_count(self, backdoor, values):
        count = min(self.count, backdoor.task_count())
        return max(0, count - len(values))

    def summarize(self, values):
        return {}

    def __info__(self):
        return {
            **super().__info__(),
            'count': self.count
        }


__all__ = [
    'Const'
]
