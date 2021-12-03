from ..instance import *


class PHP(Instance):
    base = 2
    tag = 'php'

    def __init__(self, p, h):
        self.type = '%d_%d' % (p, h)
        self.name = 'Instance: PHP (%d pigeons, %d holes)' % (p, h)
        self.cnf_path = self.build_cnf_path(self.tag, 'php-%d-%d' % (p, h))
        super().__init__(secret_key=SecretKey(1, p * h))


class MatrixPHP(Instance):
    tag = 'mphp'

    def __init__(self, h, p):
        self.base = p
        self.type = '%d_%d' % (h, p)
        self.name = 'Instance: Matrix PHP (%d pigeons, %d holes)' % (p, h)
        self.x_path = self.build_x_map_path('php', 'matrix', 'chr_%s' % self.type)
        self.cnf_path = self.build_cnf_path('php', 'matrix', 'chr_%s' % self.type)
        super().__init__(secret_key=SecretKey(0, h))


__all__ = [
    'PHP',
    'MatrixPHP'
]
