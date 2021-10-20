from .impl import spaces

from util import load_modules


def Space(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(**configuration)
    return spaces.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Space'
]
