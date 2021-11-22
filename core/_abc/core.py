class Core:
    slug = None
    name = 'Core'

    def __init__(self, limit, output, executor, instance, *args, **kwargs):
        self.limit = limit
        self.output = output
        self.executor = executor
        self.instance = instance

    def launch(self, *args, **kwargs):
        raise NotImplementedError

    def queue(self, point, sampling):
        backdoor = point.backdoor


__all__ = [
    'Core'
]
