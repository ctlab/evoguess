from ._abc import Function
from .impl import functions
from .module import modules, measure, solver

from util import load_modules


def FunctionBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(modules, **configuration)
    return functions.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Function',
    # modules
    'solver',
    'measure',
    # builder
    'FunctionBuilder'
]
