from .cipher import *
from instance.impl.instance import *

instances = {
    Instance.slug: Instance,
    StreamCipher.slug: StreamCipher
}

__all__ = [
    'instances',
    # impls
    'Instance',
    'StreamCipher',
]
