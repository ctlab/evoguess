from typing import Tuple
from ..typings import Point, Vector
from method.typings.handle import Handle
from instance.typings.variables import Backdoor

from time import time as now
from util.collection import for_each


class Algorithm:
    slug = None
    name = 'Algorithm'

    def __init__(self, limit, output, method, instance, *args, **kwargs):
        self.limit = limit
        self.output = output
        self.method = method
        self.instance = instance
        self.start_stamp = None

    def preprocess(self, *points: Point) -> Vector:
        raise NotImplementedError

    def process(self, estimated: Vector) -> Vector:
        raise NotImplementedError

    def start(self, *points: Point) -> Vector:
        self.start_stamp = now()
        self.output.open('algorithm')
        self.output.info(**self.__info__())
        self.output.debug(1, 0, f'Algorithm start on {self.start_stamp}')

        # preprocess
        vector, preprocess_stamp = self.preprocess(*points), now()
        self.limit.set('time', preprocess_stamp - self.start_stamp)
        self.output.debug(1, 1, f'Initial vector with {len(vector)} point(s):')
        for_each(vector, lambda point: self.output.debug(1, 2, point.to_dict()))
        self.output.debug(1, 1, f'Algorithm end preprocess on {preprocess_stamp}')

        # process
        solution, process_stamp = self.process(vector), now()
        self.output.debug(1, 1, f'Found solution with {len(solution)} point(s):')
        for_each(solution, lambda point: self.output.debug(1, 2, point.to_dict()))
        self.output.debug(1, 1, f'Algorithm end process on {process_stamp}')

        self.method.executor.shutdown()
        self.output.close()
        return solution

    def start_from_vector(self, vector: Vector) -> Vector:
        return self.start(*vector)

    def start_from_backdoors(self, *backdoors: Backdoor) -> Vector:
        return self.start(*map(Point, backdoors))

    def _queue(self, point: Point) -> Tuple[Point, Handle]:
        return point, self.method.queue(self.instance, point.backdoor)

    def _proceed_index_result(self, index: int, vector: Vector):
        replace = self.output.make_replace([p.backdoor for p in vector])
        self.output.log({
            'index': index,
            'spent': round(self.limit.get('time'), 2),
            'points': [point.to_dict(replace) for point in vector]
        })

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'limit': self.limit.__info__(),
            'method': self.method.__info__(),
            'instance': self.instance.__info__()
        }

    def __str__(self):
        return self.name


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    'Algorithm'
]
