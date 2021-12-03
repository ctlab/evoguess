from ..instance import *

ks_st = {
    0: 1306,
    1: 1786,
}


class Grain(StreamCipher):
    base = 2
    tag = 'grain'

    def __init__(self, v):
        self.type = 'v%d' % v
        self.name = 'Cipher: Grain v%d' % v
        self.cnf_path = self.build_cnf_path(self.tag, 'grain_v%d' % v)
        super().__init__(
            secret_key=SecretKey(1, 160),
            key_stream=KeyStream(ks_st[v], 160)
        )


__all__ = [
    'Grain',
]
