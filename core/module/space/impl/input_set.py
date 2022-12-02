from ..space import Space

from instance.module.variables import Backdoor
from instance.impl.cipher_s import StreamCipher


class InputSet(Space):
    slug = 'space:input_set'

    # noinspection PyProtectedMember
    def get_backdoor(self, cipher: StreamCipher) -> Backdoor:
        return Backdoor(
            from_vars=cipher.input_set._vars,
            from_file=cipher.input_set.filepath,
        )

    def __config__(self):
        return {
            'slug': self.slug,
            'by_mask': self.by_mask,
            'by_string': self.by_string
        }


__all__ = [
    'InputSet'
]
