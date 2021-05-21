from .instance import *


class StreamCipher(Instance):
    slug = 'cipher:stream'
    name = 'Stream Cipher'

    def __init__(self, key_stream, *args, **kwargs):
        self.key_stream = key_stream
        super().__init__(*args, **kwargs)

    @staticmethod
    def has_intervals():
        return True

    def intervals(self):
        return [self.key_stream]

    def __info__(self):
        return {
            **super().__info__(),
            'key_stream': self.key_stream.__info__()
        }


__all__ = [
    'StreamCipher'
]
