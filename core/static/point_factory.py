from ..typings.point import Point


class PointFactory:
    def __init__(self):
        self.comparator = None

    def configure(self, comparator):
        self.comparator = comparator

    def produce(self, backdoor):
        assert self.comparator, "Comparator not set"
        return Point(self.comparator, backdoor)


FACTORY = PointFactory()

__all__ = [
    'FACTORY',
]
