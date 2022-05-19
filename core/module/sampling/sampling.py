from function.typings import Results


class Sampling:
    slug = 'sampling'
    name = 'Sampling'

    def __init__(self, max_size: int, *args, **kwargs):
        # self.order = order
        self.regions = 1024
        self.max_size = max_size
        # todo: regions settings

    def get_state(self, offset: int, size: int) -> 'SamplingState':
        return SamplingState(self, offset, size)

    def generate(self, power: int, values: list[float]):
        raise NotImplementedError

    def summarize(self, values: list[float]):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            # 'order': self.order
        }

    def __str__(self):
        return self.name


class SamplingState:
    def __init__(self, sampling: Sampling, offset: int, size: int):
        self.size = size
        self.offset = offset
        self.sampling = sampling

    def chunks(self, results: Results) -> list[tuple[int, int]]:
        self.offset = 0
        return [(0, 0)]


__all__ = [
    'Sampling',
    'SamplingState'
]
