from .cipher import *
from .instance import *

instances = {
    Instance.slug: Instance,
    StreamCipher.slug: StreamCipher
}

__all__ = [
    'Instance',
    'StreamCipher'
]
