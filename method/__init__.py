from .impl import methods
from .module import modules

from util import load_modules


def Method(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return methods.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Method',
]
