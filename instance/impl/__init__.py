from .cipher_b import *
from .cipher_s import *
from .instance import *

instances = {
    Instance.slug: Instance,
    StreamCipher.slug: StreamCipher
}

__all__ = [
    'Instance',
    'StreamCipher'
]
