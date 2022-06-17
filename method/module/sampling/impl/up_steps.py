from ..sampling import *


class UPSteps(Sampling):
    slug = 'sampling:up_steps'
    name = 'Sampling: UP Steps'

    def __init__(self, steps, *args, **kwargs):
        self.steps = steps
        self.min = kwargs['min']
        self.max = self.min << steps
        super().__init__(self.max, *args, **kwargs)

    def get_count(self, backdoor, results=()):
        count = len(results)
        bd_count = backdoor.power()

        if count == 0:
            return min(self.min, bd_count)
        elif count < bd_count and count < self.max:
            if sum([not r[4] for r in results if r]) == 0:
                bound = min(count << 1, self.max, bd_count)
                return max(0, bound - count)
        return 0

    def __info__(self):
        return {
            **super().__info__(),
            'min': self.min,
            'steps': self.steps,
        }


__all__ = [
    'UPSteps'
]
