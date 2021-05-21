from .impl import functions
from .module import modules, measure, solver

from util import load_modules


def Function(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return functions.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'solver',
    'measure',
    'Function'
]
