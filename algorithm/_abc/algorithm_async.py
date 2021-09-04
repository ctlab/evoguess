from .algorithm_abc import *


class AlgorithmAsync(AlgorithmABC):
    max_pending_points = None

    def get_next_points(self, vector: Vector, count: int) -> Vector:
        raise NotImplementedError

    def update_vector(self, vector: Vector, *points: Point) -> Vector:
        raise NotImplementedError

    def process(self, estimated: Vector) -> Vector:
        p_handles = []
        while not self.limit.exhausted():
            index_value = self.limit.increase('index')
            to_process = max(0, self.max_pending_points - len(p_handles))
            p_handles.extend(map(self._queue, self.get_next_points(vector, to_process)))

            estimated, p_handles = self._await(p_handles, self.min_vector_length)
            vector = self.update_vector(vector, *estimated)
            self._proceed_index_result(index_value, vector)

        return estimated
