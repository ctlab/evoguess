from .impl import Instance, instances
from .module import modules, encoding, variables

from util import load_modules


def InstanceBuilder(configuration, **kwargs):
    slug = configuration.pop('slug')
    loaded_modules = load_modules(**modules, **configuration)
    return instances.get(slug)(**kwargs, **loaded_modules)


__all__ = [
    'Instance',
    # modules
    'encoding',
    'variables',
    # builder
    'InstanceBuilder'
]
