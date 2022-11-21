from ..space import *

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


__all__ = [
    'InputSet'
]
