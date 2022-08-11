from ..module.variables.vars import Supplements
from ..module.encoding.encoding import Encoding
from ..module.variables import Backdoor, Variables, Mask


class Instance:
    slug = 'instance'
    name = 'Instance'

    def __init__(self, encoding: Encoding, input_set: Variables):
        self.encoding = encoding
        self.input_set = input_set

    def encoding_data(self):
        return self.encoding.get_data()

    # noinspection PyProtectedMember
    def get_backdoor(self, by_string: str = None, by_mask: Mask = None):
        backdoor = Backdoor(
            from_file=self.input_set.filepath,
            from_vars=self.input_set._variables
        )
        if by_mask:
            backdoor._set_mask(by_mask)
        elif by_string:
            var_names = by_string.split()
            return backdoor._set_mask([
                1 if str(v) in var_names else
                0 for v in backdoor._variables
            ])
        return backdoor

    def get_supplements(self, *args, **kwargs) -> Supplements:
        return [], []

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'encoding': self.encoding.__info__(),
            'input_set': self.input_set.__info__(),
        }


__all__ = [
    'Instance'
]
