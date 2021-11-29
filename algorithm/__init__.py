from .impl import algorithms
from .module import modules, evolution

from util import load_modules


def Algorithm(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return algorithms.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Algorithm',
    # modules
    'evolution'
]
