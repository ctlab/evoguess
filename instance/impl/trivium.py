from ..instance import *


class Bivium(StreamCipher):
    base = 2
    tag = 'bivium'
    name = 'Cipher: Bivium'

    def __init__(self):
        self.cnf_path = self.build_cnf_path('trivium', self.tag)
        super().__init__(
            secret_key=SecretKey(1, 177),
            key_stream=KeyStream(443, 200)
        )


class Trivium_64(StreamCipher):
    tag = 'trivium'
    name = 'Cipher: Trivium 64/75'

    def __init__(self):
        self.type = '64_75'
        self.path = self.build_path(self.tag, 'trivium_64')
        super().__init__(
            secret_key=SecretKey(1, 64),
            key_stream=KeyStream(398, 75)
        )


class Trivium_96(StreamCipher):
    tag = 'trivium'
    name = 'Cipher: Trivium 96/100'

    def __init__(self):
        self.type = '96_100'
        self.path = self.build_path(self.tag, 'trivium_96')
        super().__init__(
            secret_key=SecretKey(1, 96),
            key_stream=KeyStream(530, 100)
        )


class Trivium(StreamCipher):
    tag = 'trivium'
    name = 'Cipher: Trivium'

    def __init__(self):
        self.type = '288_300'
        self.path = self.build_path(self.tag, 'trivium')
        super().__init__(
            secret_key=SecretKey(1, 288),
            key_stream=KeyStream(1588, 300)
        )


__all__ = [
    'Bivium',
    'Trivium',
    'Trivium_64',
    'Trivium_96'
]
