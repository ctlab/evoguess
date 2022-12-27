from .instance import *


class StreamCipher(Instance):
    slug = 'cipher:stream'
    name = 'Stream Cipher'

    def __init__(self, supbs, output_set, *args, **kwargs):
        self.supbs = supbs
        self.output_set = output_set
        super().__init__(*args, **kwargs)

    @staticmethod
    def has_intervals():
        return True

    def intervals(self):
        return [self.output_set]

    def __info__(self):
        return {
            **super().__info__(),
            'supbs': self.supbs.__info__(),
            'output_set': self.output_set.__info__()
        }


__all__ = [
    'StreamCipher'
]
