from .impl import cores
from .module import modules, limitation, sampling, comparator

from util import load_modules


def Core(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return cores.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Core',
    # modules
    'limit',
    'sampling',
    'comparator',
]
