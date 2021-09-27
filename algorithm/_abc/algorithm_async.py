from .algorithm_abc import *


class AlgorithmAsync(AlgorithmABC):
    max_points = None
    await_count = None
    name = 'Algorithm(Async)'

    def get_points(self, vector: Vector, count: int) -> Vector:
        raise NotImplementedError

    def update_vector(self, vector: Vector, *points: Point) -> Vector:
        raise NotImplementedError

    def process(self, estimated: Vector) -> Vector:
        p_handles, vector = [], estimated
        while not self.limit.exhausted():
            index = self.limit.increase('index')
            if self.max_points > len(p_handles):
                count = self.max_points - len(p_handles)
                p_handles.extend(map(self._queue, self.get_points(vector, count)))

            estimated, p_handles = self._await(*p_handles, count=self.await_count)
            vector = self.update_vector(vector, *estimated)
            self._proceed_index_result(index, vector)
            self._update_best(*estimated)
        self._cancel(p_handles)
        return vector


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'AlgorithmAsync',
]
