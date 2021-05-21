def load_modules(modules=(()), **kwargs):
    modules, loaded_kwargs = dict(modules), {}
    for key, value in kwargs.items():
        if isinstance(value, dict):
            slug = value.pop('slug')
            value = modules[slug](**load_modules(modules, **value))
        loaded_kwargs[key] = value
    return loaded_kwargs


def _key(function):
    return str(function).split()[1].lower()


def build(structure, **kwargs):
    constructor, dependencies = list(structure.items())[0]
    key = _key(constructor)
    return key, constructor(kwargs[key], **dict([
        build(dependency, **kwargs) if isinstance(dependency, dict) else
        (_key(dependency), dependency(kwargs[_key(dependency)]))
        for dependency in dependencies
    ]))


__all__ = [
    'array',
    'caster',
    'bitmask',
    'numeral',
    #
    'build',
    'load_modules',
]
