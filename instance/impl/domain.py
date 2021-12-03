from ..instance import *


class Domain(Instance):
    tag = 'domain'

    def __init__(self, base):
        self.base = base
        self.type = str(base)
        self.name = 'Instance: Domain (base: %d)' % base
        self.x_path = self.build_x_map_path(self.tag, self.type)
        self.cnf_path = self.build_cnf_path(self.tag, self.type)
        super().__init__(secret_key=SecretKey(0, 2012))


__all__ = [
    'Domain'
]
