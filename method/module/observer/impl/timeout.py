from ..observer import *


class Timeout(Observer):
    slug = 'observer:timeout'
    name = 'Observer: Timeout'


__all__ = [
    'Timeout'
]
