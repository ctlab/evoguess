from function.typings import Results
from util.array import concat


class Sampling:
    slug = 'sampling'
    name = 'Sampling'

    def __init__(self, max_size: int, split_into: int, *args, **kwargs):
        self.max_size = max_size
        self.split_into = split_into

    def get_state(self, offset: int, size: int) -> 'SamplingState':
        return SamplingState(self, offset, size)

    def get_count(self, offset: int, size: int, results: Results):
        raise NotImplementedError

    def summarize(self, results: Results):
        raise NotImplementedError

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }

    def __str__(self):
        return self.name


class SamplingState:
    def __init__(self, sampling: Sampling, offset: int, size: int):
        self.size = size
        self.offset = offset
        self.sampling = sampling

    def chunks(self, results: Results) -> list[tuple[int, int]]:
        count = self.sampling.get_count(self.offset, self.size, results)
        size, remainder = divmod(count, self.sampling.split_into)
        chunks = []
        for chunk_i in range(0, self.sampling.split_into):
            chunk_size = size + 1 if chunk_i < remainder else 0
            chunks.append((self.offset, chunk_size))
            self.offset += chunk_size
        return chunks


__all__ = [
    'Sampling',
    'SamplingState'
]
