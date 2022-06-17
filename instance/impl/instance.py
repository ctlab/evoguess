from ..typings import Backdoor
from ..typings.var import Supplements

from os.path import isfile
from numpy.random import RandomState


class Instance:
    slug = 'instance'
    name = 'Instance'

    def __init__(self, cnf, input_set, *args, **kwargs):
        self.cnf = cnf
        self.input_set = input_set

    def check(self):
        return isfile(self.cnf.path)

    def clauses(self, constraints=()):
        return self.cnf.clauses(constraints)

    def max_literal(self):
        return self.cnf.max_literal()

    # noinspection PyProtectedMember
    def get_backdoor(self, **kwargs):
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
            'cnf': self.cnf.__info__(),
            'input_set': self.input_set.__info__(),
        }


__all__ = [
    'Instance'
]
