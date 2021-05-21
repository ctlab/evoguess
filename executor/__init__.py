from .impl import executors
from .module import modules, shaping

from util import load_modules


def Executor(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return executors.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'shaping',
    'Executor'
]
