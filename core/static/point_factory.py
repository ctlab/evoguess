from ..typings.point import Point


class PointFactory:
    def __init__(self):
        self.comparator = None

    def configure(self, comparator):
        self.comparator = comparator

    def produce(self, backdoor):
        assert self.comparator, "Comparator not set"
        return Point(self.comparator, backdoor)


POINT_FACTORY = PointFactory()

__all__ = [
    'POINT_FACTORY',
]
