from ..instance import *


class E0(StreamCipher):
    base = 2
    tag = 'e0'
    name = 'Cipher: E0'

    def __init__(self):
        self.cnf_path = self.build_cnf_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 128),
            key_stream=KeyStream(1785, 128)
        )


__all__ = [
    'E0'
]
