from ..instance import *


class SGEN(Instance):
    base = 2
    tag = 'sgen'

    def __init__(self, v, n, seed='5-1'):
        self.type = '%d_%d_%s' % (v, v * n, seed)
        self.name = 'Instance: SGEN%d-%d (seed: %s)' % (v, v * n, seed)
        self.cnf_path = self.build_cnf_path(self.tag, 'sgen%d_%d_%s' % (v, v * n, seed))
        super().__init__(secret_key=SecretKey(1, n))


__all__ = [
    'SGEN'
]
