from .impl import preprocesses

from util import load_modules


def Preprocess(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(**configuration)
    return preprocesses.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Preprocess'
]
