from .impl import algorithms
from .portfolio import portfolio, schemas
from .module import modules, limit, tuner, evolution

from util import load_modules

algorithms = {
    **portfolio,
    **algorithms,
}

modules = {
    **modules,
    **schemas,
}


def Algorithm(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return algorithms.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'limit',
    'tuner',
    'evolution',
    'Algorithm',
]
