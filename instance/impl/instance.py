from ..typings.variables.impl import backdoors

from os.path import isfile
from util.array import side_trim
from util.operator import attreq
from util.numeral import binary_to_base


class Instance:
    slug = 'instance'
    name = 'Instance'

    def __init__(self, cnf, input_set, *args, **kwargs):
        self.cnf = cnf
        self.supbs = kwargs.get('supbs')
        self.input_set = input_set

    def __str__(self):
        return self.name

    def clauses(self):
        return self.cnf.clauses()

    def max_literal(self):
        return self.cnf.max_literal()

    def check(self):
        return isfile(self.cnf.path)

    def get_backdoor(self, slug, **kwargs):
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

        if backdoor.base > 2:
            raise Exception('Haven\'t realised')
        #     assumptions, x_map = [], XMAP.parse(self.x_path, self.key)
        #     domain_masks = domain_masks or [[1] * self.base] * len(values)
        #     for mask, var, value in zip(domain_masks, variables, values):
        #         if value >= 0:
        #             assumptions.append(x_map.get_cnf_var(var, value))
        #         else:
        #             zero_values = [i for i, bit in enumerate(mask[::-1]) if bit]
        #             zero_vars = [x_map.get_cnf_var(var, z_value) for z_value in zero_values]
        #             assumptions.extend([-var for var in zero_vars])
        else:
            assumptions = [x if values[i] else -x for i, x in enumerate(variables)]

        # todo: add intervals to assumptions
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
            # 'supbs': self.supbs.__info__(),
            'input_set': self.input_set.__info__()
        }


__all__ = [
    'Instance'
]
