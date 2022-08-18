from .cipher_b import *
from .cipher_s import *
from .instance import *

instances = {
    Instance.slug: Instance,
    BlockCipher.slug: BlockCipher,
    StreamCipher.slug: StreamCipher
}

__all__ = [
    'Instance',
    'BlockCipher',
    'StreamCipher',
]
