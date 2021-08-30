from ..sampling import *


class Const(Sampling):
    slug = 'sampling:const'
    name = 'Sampling: Const'

    def __init__(self, count: int, *args, **kwargs):
        self.count = count
        super().__init__(count, count, *args, **kwargs)

    def get_count(self, backdoor, results=()):
        count = min(self.count, backdoor.task_count())
        return max(0, count - len(results))

    def get_size(self):
        return self.count, self.count

    def report(self, values):
        return {}

    def __info__(self):
        return {
            **super().__info__(),
            'count': self.count
        }


__all__ = [
    'Const'
]
