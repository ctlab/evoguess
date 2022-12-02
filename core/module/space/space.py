from instance.impl.instance import Instance
from instance.module.variables import Mask, ByteMask, Backdoor


class Space:
    slug = 'space'

    def __init__(self,
                 by_mask: Mask = None,
                 by_string: str = None):
        self.by_mask = by_mask
        self.by_string = by_string

    def get_backdoor(self, instance: Instance) -> Backdoor:
        raise NotImplementedError

    # noinspection PyProtectedMember
    def get_initial(self, instance: Instance) -> Backdoor:
        backdoor = self.get_backdoor(instance)
        if self.by_mask is not None:
            backdoor._set_mask(self.by_mask)
        elif self.by_string is not None:
            var_names = self.by_string.split()
            backdoor._set_mask([
                1 if str(v) in var_names
                else 0 for v in backdoor._vars
            ])
        return backdoor

    # noinspection PyProtectedMember
    def unpack(self, instance: Instance, bytemask: ByteMask) -> Backdoor:
        backdoor = self.get_backdoor(instance)
        return backdoor._set_mask(Backdoor.unpack(bytemask))

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'by_mask': self.by_mask,
            'by_string': self.by_string
        }


__all__ = [
    'Space'
]