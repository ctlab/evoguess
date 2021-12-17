from instance.typings.variables.backdoor import Backdoor


class BaseBackdoor(Backdoor):
    slug = 'backdoor:base'

    def __init__(self, variables, mask, base=2):
        self.base = base
        super().__init__(variables)
        self._set_mask(mask)

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
        return BaseBackdoor(base)

    @staticmethod
    def _to_str(variables):
        return Backdoor._to_str(variables)

    @staticmethod
    def parse(string, base=2):
        return BaseBackdoor(base, _list=Backdoor._from_str(string))

    def __info__(self):
        return {
            **super().__info__(),
            'base': self.base
        }


__all__ = [
    'BaseBackdoor'
]
