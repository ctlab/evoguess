from time import time as now

from core.typings.point import Point


class _Algorithm:
    def __init__(self, point, seeds):
        pass

    def __enter__(self):
        self.start_stamp = now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Algorithm:
    slug = None
    name = 'Algorithm'

    def __init__(self):
        self.vector = None
        self.best_point = None
        self.start_stamp = None

    def configure(self, point: Point, seeds) -> _Algorithm:
        self.vector = [point]
        self.best_point = point

        return _Algorithm(point, seeds)
