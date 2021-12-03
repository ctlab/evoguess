from ..instance import *


class Volfram(StreamCipher):
    base = 2
    tag = 'volfram'
    name = 'Cipher: Volfram'

    def __init__(self):
        self.cnf_path = self.build_cnf_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 128),
            key_stream=KeyStream(12417, 128)
        )


__all__ = [
    'Volfram'
]
