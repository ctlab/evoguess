from .impl import outputs

from util import load_modules


def Output(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(**configuration)
    return outputs.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Output'
]
