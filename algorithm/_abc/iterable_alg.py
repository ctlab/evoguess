from .algorithm_abc import *


class IterableAlg(AsyncAlg):
    name = 'Iterable(Algorithm)'
    vector_length = None

    def __init__(self, *args, **kwargs):
        self.min_vector_length = self.vector_length
        self.max_pending_points = self.vector_length
        super().__init__(*args, **kwargs)

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        raise NotImplementedError

    def start_iteration(self, vector: Vector) -> Vector:
        raise NotImplementedError

    def end_iteration(self, current: Vector, new: Vector) -> Vector:
        raise NotImplementedError

    def get_next_points(self, vector: Vector, count: int) -> Vector:
        return self.start_iteration(vector) if count >= self.vector_length else []

    def update_core_vector(self, vector: Vector, *points: Point) -> Vector:
        return self.end_iteration(vector, points)


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'IterableAlg',
]
