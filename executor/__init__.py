from .impl import executors


def Executor(configuration, **kwargs):
    slug = configuration.pop('slug')
    return executors.get(slug)(**kwargs)


__all__ = [
    'Executor'
]
