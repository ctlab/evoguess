from ..typings.variables.impl import backdoors

from os.path import isfile
from util.array import side_trim
from util.operator import attreq


class Instance:
    slug = 'instance'
    name = 'Instance'

    def __init__(self, cnf, input_set, *args, **kwargs):
        self.cnf = cnf
        self.input_set = input_set
        self.extra_set = kwargs.get('extra_set')

    def __str__(self):
        return self.name

    def clauses(self, constraints=()):
        return self.cnf.clauses(constraints)

    def max_literal(self):
        return self.cnf.max_literal()

    def check(self):
        return isfile(self.cnf.path)

    def get_backdoor(self, slug='backdoor:base', **kwargs):
        if '_list' not in kwargs:
            return backdoors[slug](_list=self.input_set, **kwargs)
        else:
            _list = kwargs.pop('_list')
            if isinstance(_list, str):
                _list = backdoors[slug]._from_str(_list)
            mask = [1 if v in _list else 0 for v in self.input_set]
            return backdoors[slug](_list=self.input_set, **kwargs)._set_mask(mask)

    def get_backdoor2(self, kind, base, mask):
        Constructor = next(filter(attreq('kind', kind), backdoors.values()), None)
        backdoor = Constructor(base=base, _list=self.input_set)
        return backdoor._set_mask(mask)

    def get_bd_mask(self, backdoor):
        # assert backdoor._list == self.input_set._list
        return side_trim(backdoor.get_mask(), at_start=False)

    def get_assumptions(self, backdoor, values):
        variables = backdoor.variables()

        assumptions = [x if values[i] else -x for i, x in enumerate(variables)]
        return assumptions

    @staticmethod
    def has_intervals():
        return False

    def intervals(self):
        return []

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'cnf': self.cnf.__info__(),
            'input_set': self.input_set.__info__(),
            'extra_set': self.extra_set and self.extra_set.__info__()
        }


__all__ = [
    'Instance'
]
