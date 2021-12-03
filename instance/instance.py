from .cnf import *

from os.path import isfile, join
from utils import numeral_system as ns, array, bit_mask as bm
from structure.array import Interval, Backdoor, DomainBackdoor, DomainZBackdoor

SecretKey = Interval
PublicKey = Interval
KeyStream = Interval

base_path = './instance/cnf/template'


class Instance:
    tag = None
    base = None
    type = None
    x_path = None
    cnf_path = None
    name = 'Instance'

    def __init__(self,
                 secret_key: SecretKey
                 ):
        self.secret_key = secret_key
        self.key = self.tag if self.type is None else '%s_%s' % (self.tag, self.type)

    def __str__(self):
        return self.name

    def cnf(self):
        return CNF.parse(self.cnf_path, self.key)

    def clauses(self):
        return self.cnf().clauses

    def check(self):
        return isfile(self.cnf_path)

    def get_bd_bits(self, backdoor):
        if backdoor.type == 1:
            domain_masks = []
            bd_mask = [bm.to_bit(sk_var in backdoor) for sk_var in self.secret_key]
        else:
            snapshot = backdoor.snapshot()
            bd_vars, domain_masks = array.unzip(snapshot)
            bd_mask = [bm.to_bit(sk_var in bd_vars) for sk_var in self.secret_key]
        return array.trim(bd_mask, at_start=False), array.concat(*domain_masks)

    def prepare_simple_bd(self, bd_mask, domain_mask):
        variables = self.secret_key.filter(bd_mask)
        domain_mask = domain_mask[:self.base * len(variables)]
        domain_masks = array.chunk_slice(self.base, domain_mask)
        return variables, domain_masks

    def get_assumptions(self, simple_bd, values_bits):
        variables, domain_masks = simple_bd
        values = ns.binary_to_base(self.base + 1, values_bits[0])

        assert len(values) >= len(variables)
        values = [value - 1 for value in values[:len(variables)]]

        if self.base > 2:
            assumptions, x_map = [], XMAP.parse(self.x_path, self.key)
            domain_masks = domain_masks or [[1] * self.base] * len(values)
            for mask, var, value in zip(domain_masks, variables, values):
                if value >= 0:
                    assumptions.append(x_map.get_cnf_var(var, value))
                else:
                    zero_values = [i for i, bit in enumerate(mask[::-1]) if bit]
                    zero_vars = [x_map.get_cnf_var(var, z_value) for z_value in zero_values]
                    assumptions.extend([-var for var in zero_vars])
        else:
            assumptions = [x if values[i] else -x for i, x in enumerate(variables)]

        return assumptions

    def get_backdoor(self, line):
        if line == '*':
            return self.secret_key.to_backdoor(self.base)

        for Constructor in [
            Backdoor,
            DomainBackdoor,
            DomainZBackdoor
        ]:
            try:
                return Constructor.parse(self.base, line)
            except ValueError:
                pass

        return None

    def load_backdoors(self, path):
        with open(path) as f:
            lines = [ln.strip() for ln in f.readlines()]
            return [self.get_backdoor(ln) for ln in lines if len(ln) > 0]

    @staticmethod
    def has_intervals():
        return False

    def intervals(self):
        return []

    @staticmethod
    def build_cnf_path(*args):
        return join(base_path, *args) + '.cnf'

    @staticmethod
    def build_x_map_path(*args):
        return join(base_path, *args) + '-x.pickle'


class Cipher(Instance):
    tag = None
    path = None
    name = 'Cipher'

    def __init__(self,
                 secret_key: SecretKey,
                 key_stream: KeyStream
                 ):
        super().__init__(secret_key)
        self.key_stream = key_stream

    @staticmethod
    def has_intervals():
        return True

    def intervals(self):
        return [self.key_stream]


StreamCipher = Cipher


class BlockCipher(Cipher):
    def __init__(self,
                 secret_key: SecretKey,
                 public_key: PublicKey,
                 key_stream: KeyStream
                 ):
        super().__init__(secret_key, key_stream)
        self.public_key = public_key

    def intervals(self):
        return [self.public_key, self.key_stream]


__all__ = [
    'Cipher',
    'Instance',
    'SecretKey',
    'PublicKey',
    'KeyStream',
    'BlockCipher',
    'StreamCipher'
]
