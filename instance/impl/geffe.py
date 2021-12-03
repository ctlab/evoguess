from ..instance import *


class Geffe(StreamCipher):
    base = 2
    tag = 'geffe'
    name = 'Cipher: Geffe'

    def __init__(self):
        self.cnf_path = self.build_cnf_path(self.tag)
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(301, 100)
        )


__all__ = [
    'Geffe'
]
