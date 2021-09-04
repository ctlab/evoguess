from .algorithm_abc import *


class StreamingAlg(AsyncAlg):
    name = 'Algorithm(Streaming)'
    min_vector_length = None
    max_pending_points = None

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        raise NotImplementedError

    def get_next_points(self, vector: Vector, count: int) -> Vector:
        raise NotImplementedError

    def update_core_vector(self, vector: Vector, *points: Point) -> Vector:
        raise NotImplementedError

    def postprocess(self, solution: Vector):
        raise NotImplementedError


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'StreamingAlg',
]
