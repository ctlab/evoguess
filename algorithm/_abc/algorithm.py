from time import time as now

from core.typings.point import Point


class _IAlgorithm:
    pass


class Algorithm:
    slug = None
    name = 'Algorithm'

    def __init__(self):
        self.vector = None
        self.best_point = None
        self.start_stamp = None

    def start(self, point: Point) -> _IAlgorithm:
        self.vector = [point]
        self.best_point = point

    def __enter__(self):
        self.start_stamp = now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
