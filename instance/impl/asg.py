from ..instance import *

ks_st = {
    (72, 76): 3351,
    (96, 112): 6547,
    (192, 200): 22506
}


class ASG(StreamCipher):
    base = 2
    tag = 'asg'

    def __init__(self, sk, ks):
        self.type = '%d_%d' % (sk, ks)
        self.name = 'Cipher: ASG %d/%d' % (sk, ks)
        self.cnf_path = self.build_cnf_path(self.tag, 'asg_%d_%d' % (sk, ks))
        super().__init__(
            secret_key=SecretKey(1, sk),
            key_stream=KeyStream(ks_st[(sk, ks)], ks)
        )


__all__ = [
    'ASG'
]
