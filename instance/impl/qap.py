from ..instance import *


class QAP(Instance):
    tag = 'qap'

    def __init__(self, base):
        self.base = base
        self.type = str(base)
        self.name = 'Instance: QAP (base: %d)' % base
        self.x_path = self.build_x_map_path(self.tag, self.type)
        self.cnf_path = self.build_cnf_path(self.tag, self.type)
        super().__init__(secret_key=SecretKey(0, base))


__all__ = [
    'QAP'
]
