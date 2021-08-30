from ..sampling import *


class UPSteps(Sampling):
    slug = 'sampling:up_steps'
    name = 'Sampling: UP Steps'

    def __init__(self, step: int, *args, **kwargs):
        self.step = step
        self.min, self.max = kwargs['min'], kwargs['max']
        super().__init__(self.max, step, *args, **kwargs)

    def get_count(self, backdoor, results=()):
        count = len(results)
        bd_count = backdoor.task_count()

        if count == 0:
            return min(self.min, bd_count)
        elif count < bd_count and count < self.max:
            if sum([not r[4] for r in results if r]) == 0:
                bound = min(count + self.step, self.max, bd_count)
                return max(0, bound - count)
        return 0

    def __info__(self):
        return {
            **super().__info__(),
            'min': self.min,
            'max': self.max,
            'step': self.step,
        }


__all__ = [
    'UPSteps'
]
