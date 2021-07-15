from instance.typings.variables.backdoor import Backdoor


class BaseBackdoor(Backdoor):
    slug = 'backdoor:base'

    def __init__(self, base=2, _list=()):
        self.base = base
        super().__init__(_list)

    def get_copy(self, mask):
        backdoor = BaseBackdoor(self.base, self._list)
        return backdoor._set_mask(mask)

    def get_bases(self):
        return [self.base] * len(self)

    def task_count(self):
        return self.base ** len(self)

    def get_masks(self):
        return [(2 ** self.base - 1) << 1] * len(self)

    def get_mappers(self):
        return [list(range(1, self.base + 1))] * len(self)

    @staticmethod
    def empty(base):
        return Backdoor(base)

    def __info__(self):
        return {
            **super().__info__(),
            'base': self.base
        }


__all__ = [
    'BaseBackdoor'
]
