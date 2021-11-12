from .algorithm_abc import *


class AlgorithmIterable(AlgorithmABC):
    max_points = None
    awaited_count = None
    name = 'Algorithm(Async)'

    def iteration(self, vector: Vector) -> Vector:
        raise NotImplementedError

    def process(self, estimated: Vector) -> Vector:
        while not self.limit.exhausted():
            index = self.limit.increase('index')
            estimated = self.iteration(estimated)
            self._proceed_index_result(index, estimated)
            self._update_best(*estimated)
        return estimated


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'AlgorithmIterable',
]
