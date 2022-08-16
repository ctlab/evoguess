from ..module.variables.vars import Supplements
from ..module.encoding.encoding import Encoding
from ..module.variables import Backdoor, Variables, Mask


class Instance:
    slug = 'instance'

    def __init__(self, encoding: Encoding, search_set: Variables, **kwargs):
        self.encoding = encoding
        self.search_set = search_set

    def encoding_data(self):
        return self.encoding.get_data()

    # noinspection PyProtectedMember
    def get_backdoor(self, by_string: str = None, by_mask: Mask = None):
        backdoor = Backdoor(
            from_file=self.search_set.filepath,
            from_vars=self.search_set._variables
        )
        if by_mask is not None:
            backdoor._set_mask(by_mask)
        elif by_string is not None:
            var_names = by_string.split()
            return backdoor._set_mask([
                1 if str(v) in var_names else
                0 for v in backdoor._variables
            ])
        return backdoor

    def get_supplements(self, *args: Variables, **kwargs) -> Supplements:
        return [], []

    def __str__(self):
        return self.slug

    def __info__(self):
        return {
            'slug': self.slug,
            'encoding': self.encoding.__info__(),
            'search_set': self.search_set.__info__(),
        }


__all__ = [
    'Instance'
]
