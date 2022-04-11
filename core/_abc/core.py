from numpy.random import randint, RandomState


class Core:
    slug = None
    name = 'Core'

    def __init__(self, instance, executor, output, limitation, *args, **kwargs):
        self.output = output
        self.executor = executor
        self.instance = instance
        self.limitation = limitation

        self.job_counter = 0
        self.start_stamp = None
        self.random_seed = kwargs.get('seed', randint(2 ** 32 - 1))
        self.random_state = RandomState(seed=self.random_seed)
        super().__init__(*args, **kwargs)

    def launch(self, *args, **kwargs):
        raise NotImplementedError


__all__ = [
    'Core'
]
