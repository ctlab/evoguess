from .impl import executors


def Executor(configuration, **kwargs):
    slug = configuration.pop('slug')
    # loaded_modules = load_modules(modules, **configuration)
    return executors.get(slug)(**kwargs)


__all__ = [
    'Executor'
]
