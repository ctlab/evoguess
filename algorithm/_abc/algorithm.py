from typing import Tuple
from ..typings import Point, Vector
from method.typings.handler import Handle
from instance.typings.variables import Backdoor

from time import time as now
from util.array import for_each


class Algorithm:
    name = 'Algorithm'
    slug = None

    def __init__(self, limit, output, method, instance, *args, **kwargs):
        self.limit = limit
        self.output = output
        self.method = method
        self.instance = instance

        self.start_stamp = None

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        raise NotImplementedError

    def process(self, vector: Vector) -> Vector:
        raise NotImplementedError

    def postprocess(self, solution: Vector):
        raise NotImplementedError

    def start(self, *backdoors: Backdoor) -> Vector:
        self.start_stamp = now()
        self.output.open('algorithm')
        self.output.info(**self.__info__())
        self.output.debug(1, 0, f'Algorithm start on {self.start_stamp}')

        # preprocess
        vector, preprocess_stamp = self.preprocess(*backdoors), now()
        self.limit.set('time', preprocess_stamp - self.start_stamp)
        self.output.debug(1, 1, f'Initial vector with {len(vector)} point(s):')
        for_each(vector, lambda point: self.output.debug(1, 2, point.to_dict()))
        self.output.debug(1, 1, f'Algorithm end preprocess on {preprocess_stamp}')

        # process
        solution, process_stamp = self.process(vector), now()
        self.output.debug(1, 1, f'Algorithm end process on {process_stamp}')

        # postprocess
        _, postprocess_stamp = self.postprocess(solution), now()
        self.output.debug(1, 1, f'Found solution with {len(solution)} point(s):')
        for_each(solution, lambda point: self.output.debug(1, 2, point.to_dict()))
        self.output.debug(1, 1, f'Algorithm end postprocess on {postprocess_stamp}')

        self.output.debug(1, 0, f'Algorithm end on {now()}')
        self.output.close()
        return solution

    def start_from_point(self, point: Point) -> Vector:
        # todo: provide backdoor value
        return self.start(point.backdoor)

    def start_from_vector(self, vector: Vector) -> Vector:
        # todo: provide backdoor values
        return self.start(*[p.backdoor for p in sorted(vector)])

    def _queue(self, point: Point) -> Tuple[Point, Handle]:
        return point, self.method.queue(self.instance, point.backdoor)

    def _proceed_index_result(self, index, vector):
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
