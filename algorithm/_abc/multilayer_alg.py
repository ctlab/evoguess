from .async_alg import *


class MultilayerAlg(AsyncAlg):
    min_vector_length = 1
    name = 'Algorithm(Multilayer)'

    def __init__(self, *args, **kwargs):
        self.layers = {}
        super().__init__(*args, **kwargs)

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        raise NotImplementedError

    # def get_next_points(self, vector: Vector, count: int) -> Vector:
    #     raise NotImplementedError
    #
    # def update_core_vector(self, vector: Vector, *points: Point) -> Vector:
    #     raise NotImplementedError

    def postprocess(self, solution: Vector):
        raise NotImplementedError

    def get_next_points(self, vector: Vector, count: int) -> Vector:
        raise NotImplementedError

    def update_core_vector(self, vector: Vector, *points: Point) -> Vector:
        raise NotImplementedError
