from .impl import instances
from .typings import types

from util import load_modules


def Instance(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(types, **configuration)
    return instances.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Instance'
]
