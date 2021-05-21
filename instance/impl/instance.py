from .._type.variables.impl import BaseBackdoor

from itertools import compress
from os.path import isfile, join

from util.bitmask import to_bit
from util.numeral import binary_to_base
from util.array import unzip, concat, side_trim, chunk_slice


class Instance:
    slug = 'instance'
    name = 'Instance'

    def __init__(self, cnf, secret_key):
        self.cnf = cnf
        self.secret_key = secret_key

    def __str__(self):
        return self.name

    def clauses(self):
        return self.cnf.clauses()

    def check(self):
        return isfile(self.cnf.path)

    def get_bd_bits(self, backdoor):
        if isinstance(backdoor, BaseBackdoor):
            domain_masks = []
            bd_mask = [to_bit(sk_var in backdoor) for sk_var in self.secret_key]
        else:
            snapshot = backdoor.snapshot()
            bd_vars, domain_masks = unzip(snapshot)
            bd_mask = [to_bit(sk_var in bd_vars) for sk_var in self.secret_key]
        return side_trim(bd_mask, at_start=False), concat(*domain_masks)

    def prepare_simple_bd(self, bd_mask, domain_mask):
        self_base = 2
        variables = list(compress(self.secret_key, bd_mask))
        domain_masks = chunk_slice(self_base, domain_mask)
        return variables, domain_masks[:len(variables)]

    def get_assumptions(self, simple_bd, values_bits):
        self_base = 2
        variables, domain_masks = simple_bd
        values = binary_to_base(self_base + 1, values_bits[0])

        assert len(values) >= len(variables)
        values = [value - 1 for value in values[:len(variables)]]
        # todo: convert bits[2:] to base values

        if self_base > 2:
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
            'secret_key': self.secret_key.__info__()
        }


__all__ = [
    'Instance'
]
