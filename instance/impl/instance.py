from ..typings import Backdoor
from ..typings.var import Supplements

from os.path import isfile
from numpy.random import RandomState


class Instance:
    slug = 'instance'
    name = 'Instance'

    def __init__(self, encoding, input_set, *args, **kwargs):
        self.encoding = encoding
        self.input_set = input_set

    def encoding_data(self):
        return self.encoding.get_data()

    # noinspection PyProtectedMember
    def get_backdoor(self, **kwargs):
        # todo: remove in island based fw
        if not self.input_set._variables:
            backdoor = Backdoor.from_file(self.input_set._path)
        else:
            #
            backdoor = Backdoor(self.input_set.variables())
        if 'variables' in kwargs:
            variables = kwargs['variables']
            if isinstance(variables, str):
                variables = variables.split(' ')
            else:
                raise NotImplementedError

            return backdoor._set_mask([
                1 if str(v) in variables else
                0 for v in backdoor._variables
            ])
        elif 'mask' in kwargs:
            backdoor._set_mask(kwargs['mask'])

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
