from .algorithm import *

from time import time as now
from method._type.handler import n_completed


class AsyncAlg(Algorithm):
    name = 'Async(Algorithm)'
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

    def process(self, vector: Vector) -> Vector:
        index_num = self.limit.set('index', 0)
        point_handles = [
            (point, self.method.queue(self.instance, point.backdoor))
            for point in vector if not point.estimated
        ]
        vector = [point for point in vector if point.estimated]

        if point_handles and self.min_vector_length > len(vector):
            pending_points = self.min_vector_length - len(vector)
            estimated, point_handles = self._await(point_handles, pending_points)
            vector.extend(estimated)
        self._proceed_index_result(index_num, vector)

        while not self.limit.exhausted():
            index_num = self.limit.increase('index')
            to_process = max(0, self.max_pending_points - len(point_handles))
            self.output.debug(1, 1, f'Index {index_num} will get {to_process} new points')
            point_handles.extend([
                (point, self.method.queue(self.instance, point.backdoor))
                for point in self.get_next_points(vector, to_process)
            ])
            new_job_ids = [h.job.job_id for _, h in point_handles[-to_process:]]
            self.output.debug(1, 1, f'Index {index_num} get jobs: {new_job_ids}')
            self.output.debug(1, 1, f'Index {index_num} with {len(point_handles)} handles')
            points, point_handles = self._await(point_handles, self.min_vector_length)
            self.output.debug(1, 1, f'Index {index_num} with {len(points)} estimated points')

            vector = self.update_core_vector(vector, *points)
            self._proceed_index_result(index_num, vector)

        return vector

    def _await(self, point_handles, count):
        count = min(count, len(point_handles))
        timeout = self.limit.left().get('time')
        handles = [h for (_, h) in point_handles]
        self.output.debug(1, 2, f'Wait {len(set(handles))} handles with {count}')
        done = n_completed(handles, count, timeout)
        self.output.debug(1, 2, f'Complete {len(done)} of {count}: {[h.job.job_id for h in done]}')
        self.limit.set('time', now() - self.start_stamp)

        if len(done) < count:
            all_handles = [
                point.set(**handle.result()) if handle in done
                else point.set(**handle.cancel_and_result())
                for point, handle in point_handles
            ]
            return all_handles, []

        estimated, left_point_handles = [], []
        for point, handle in point_handles:
            if handle not in done:
                left_point_handles.append((point, handle))
            else:
                estimated.append(point.set(**handle.result()))

        return estimated, left_point_handles


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'AsyncAlg',
]
