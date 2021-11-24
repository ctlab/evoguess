from numpy.random import randint, RandomState


class Core:
    slug = None
    name = 'Core'

    def __init__(self, limit, output, executor, instance, *args, **kwargs):
        self.limit = limit
        self.output = output
        self.executor = executor
        self.instance = instance

        self.job_counter = 0
        self.seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.seed)
        super().__init__(*args, **kwargs)

    def launch(self, *args, **kwargs):
        raise NotImplementedError

    # def _queue(self, backdoor) -> Handle:
    #     return self.method.queue(self.instance, point.backdoor)


__all__ = [
    'Core'
]
