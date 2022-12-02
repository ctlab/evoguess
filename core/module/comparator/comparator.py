from typing import Any


class Comparator:
    slug = None

    def compare(self, obj1: Any, obj2: Any) -> int:
        raise NotImplementedError

    def __str__(self):
        return self.slug


__all__ = [
    'Comparator'
]
