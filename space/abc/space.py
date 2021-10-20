from __future__ import annotations

from instance.typings.variables import BaseBackdoor


class Space:
    slug = 'space'
    name = 'Space'

    def __init__(self, ):
        self.variables = None

    def create(self, instance) -> Space:
        raise NotImplementedError

    def expand(self) -> Space:
        raise NotImplementedError

    def get(self) -> BaseBackdoor:
        raise NotImplementedError


__all__ = [
    'Space',
    # types
    'BaseBackdoor',
]
