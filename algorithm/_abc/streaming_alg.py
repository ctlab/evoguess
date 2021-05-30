from .algorithm import *

from time import time as now
from method._type.futures import first_completed


class StreamingAlg(Algorithm):
    in_process_count = None
    name = 'Algorithm(Streaming)'

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        raise NotImplementedError

    def get_next_points(self, vector: Vector, count: int) -> Vector:
        raise NotImplementedError

    def append_points(self, vector: Vector, *points: Point) -> Vector:
        raise NotImplementedError

    def postprocess(self, solution: Vector):
        raise NotImplementedError

    def process(self, vector: Vector) -> Vector:
        gen_number = self.limit.set('generation', 0)
        point_futures = [
            (point, self.method.queue(self.instance, point.backdoor))
            for point in vector if not point.estimated
        ]
        vector = [point for point in vector if point.estimated]
        if len(vector) == 0:
            vector, point_futures = self._await_point_futures(point_futures)
        self._process_generation_result(gen_number, vector)

        while not self.limit.exhausted():
            if len(point_futures) < self.in_process_count:
                to_process = self.in_process_count - len(point_futures)
                point_futures.extend([
                    (point, self.method.queue(self.instance, point.backdoor))
                    for point in self.get_next_points(vector, to_process)
                ])
            points, point_futures = self._await_point_futures(point_futures)

            vector = self.append_points(vector, *points)
            gen_number = self.limit.increase('generation')
            self._process_generation_result(gen_number, vector)

        return vector

    def _await_point_futures(self, point_futures):
        futures = [f for (p, f) in point_futures]
        timeout = self.limit.left().get('time')
        done = first_completed(futures, timeout)
        self.limit.set('time', now() - self.start_stamp)

        if len(done) == 0:
            canceled = [
                point.set(**future.cancel_and_result())
                for point, future in point_futures
            ]
            return canceled, []

        estimated, left_point_futures = [], []
        for point, future in point_futures:
            if future not in done:
                left_point_futures.append((point, future))
            else:
                estimated.append(point.set(**future.result()))

        return estimated, left_point_futures

    def _process_generation_result(self, number, vector):
        self.output.log({
            'generation': number,
            'spent_time': self.limit.get('time'),
            'points': [point.to_dict() for point in vector]
        })


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'StreamingAlg',
]
