from .algorithm import *

from time import time as now
from util.caster import inf_none


class IterationFuture:
    def __init__(self, point_futures, callback=None):
        self.callback = callback
        self.point_futures = point_futures

    def result(self, timeout=None):
        timeout_stamp = now() + inf_none(timeout)
        for point, future in self.point_futures:
            future_timeout = max(0, timeout_stamp - now())
            estimation = future.result(inf_none(future_timeout))
            point.set(**estimation)

        vector = [p for p, _ in self.point_futures]
        return self.callback(vector) if self.callback else vector

    def cancel_and_result(self):
        vector = []
        for point, future in self.point_futures:
            if not point.estimated:
                estimation = future.cancel_and_result()
                point.set(**estimation)
            vector.append(point)
        return self.callback(vector) if self.callback else vector


class IterableAlg(Algorithm):
    name = 'Algorithm(Iterable)'

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        raise NotImplementedError

    def iteration(self, vector: Vector) -> IterationFuture:
        raise NotImplementedError

    def postprocess(self, solution: Vector):
        raise NotImplementedError

    def process(self, vector: Vector) -> Vector:
        it_number = self.limit.set('iteration', 0)
        estimated = filter(lambda p: p.estimated, vector)
        vector = self._handle_future(IterationFuture([
            (point, self.method.queue(self.instance, point.backdoor))
            for point in vector if not point.estimated
        ]))
        self._process_iteration_result(it_number, vector)

        vector.extend(estimated)
        while not self.limit.exhausted():
            it_number = self.limit.increase('iteration')
            it_start_stamp, it_future = now(), self.iteration(vector)
            vector = self._handle_future(it_future)
            self._process_iteration_result(it_number, vector)

        return vector

    def _handle_future(self, future):
        try:
            timeout = self.limit.left().get('time')
            result = future.result(timeout=timeout)
        except TimeoutError:
            result = future.cancel_and_result()

        self.limit.set('time', now() - self.start_stamp)
        return result

    def _process_iteration_result(self, number, vector):
        self.output.log({
            'iteration': number,
            'spent_time': self.limit.get('time'),
            'points': [point.to_dict() for point in vector]
        })


__all__ = [
    'Point',
    'Vector',
    'Backdoor',
    # impl
    'IterableAlg',
    'IterationFuture'
]
