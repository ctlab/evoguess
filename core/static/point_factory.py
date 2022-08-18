from ..model.point import Point
from ..module.comparator import Comparator
from instance.module.variables import Backdoor


class PointFactory:
    def __init__(self):
        self.comparator = None

    def configure(self, comparator: Comparator):
        self.comparator = comparator

    def produce(self, backdoor: Backdoor):
        assert self.comparator, "Comparator not set"
        return Point(self.comparator, backdoor)


POINT_FACTORY = PointFactory()

__all__ = [
    'POINT_FACTORY',
]
