from typing import Any, Dict

from . import impl
from .impl import *
from .variables import *
from .vars import var_from

variables = {
    **impl.variables,
    Variables.slug: Variables,
}


def variables_from(config: Dict[str, Any]):
    slug = config.pop('slug')
    if config.get('from_vars') is not None:
        config['from_vars'] = list(map(var_from, config['from_vars']))
    return variables[slug](**config)


__all__ = [
    'Variables',
    *impl.__all__,
    # utils
    'variables_from'
]
