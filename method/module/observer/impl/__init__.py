from .timeout import Timeout

observers = {
    Timeout.slug: Timeout
}

__all__ = [
    'Timeout'
]
