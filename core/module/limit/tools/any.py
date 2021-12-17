from ..limit import *


class Any(Limit):
    slug = 'limit:any'
    name = 'Limit: Any'

    def __init__(self, **kwargs):
        super().__init__(None)
        self.args = kwargs.values()
        for arg in self.args:
            arg.limits = self.limits

    def exhausted(self) -> bool:
        return any(arg.exhausted() for arg in self.args)

    def left(self) -> dict:
        return {k: v for arg in self.args for k, v in arg.left().items()}

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            '*args': [arg.__info() for arg in self.args]
        }


__all__ = [
    'Any'
]
