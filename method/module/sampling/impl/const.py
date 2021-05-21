from ..sampling import *


class Const(Sampling):
    slug = 'sampling:const'
    name = 'Sampling: Const'

    def __init__(self, count: int):
        self.count = count

    def get_count(self, backdoor, values=()):
        # todo: filter None values
        count = min(self.count, backdoor.task_count())
        return max(0, count - len(values))

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
