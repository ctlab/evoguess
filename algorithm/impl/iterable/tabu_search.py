from ..._abc.algorithm import *

from random import shuffle
from time import time as now


class TabuSearch(Algorithm):
    slug = 'iterable:tabu'
    name = 'Algorithm(Iterable): Tabu Search'

    def __init__(self, shuffling=False, *args, **kwargs):
        self.trace = []
        self.tabu = set()
        self.shuffling = shuffling

        self.root, self.best = None, None
        super().__init__(*args, **kwargs)

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        self.root = list(map(Point, backdoors))
        self.best = sorted(self.root)[0]
        return self.root

    def process(self, vector: Vector) -> Vector:
        center, next_center = vector[-1], None
        it_number = self.limit.set('iteration', 0)
        if not center.estimated:
            future = self.method.queue(self.instance, center.backdoor)
            center.set(**future.result())
        self._process_iteration_result(it_number, vector)

        self.limit.set('time', now() - self.start_stamp)
        while not self.limit.exhausted():
            vector = self.iteration(vector)
            it_number = self.limit.increase('iteration')
            self._process_iteration_result(it_number, vector)

    def iteration(self, vector: Vector) -> Vector:
        center, next_center = vector[-1], None

        visited_points = []
        for point in self.neighbourhood(center):
            if self.is_tabu(point):
                continue

            future = self.method.queue(self.instance, point.backdoor)
            try:
                timeout = self.limit.left().get('time')
                point.set(**future.result(timeout))
            except TimeoutError:
                point.set(**future.cancel_and_result())

            self.limit.set('time', now() - self.start_stamp)
            visited_points.append(point)
            if center > point:
                next_center = point
                break

            if self.limit.exhausted():
                break

        if next_center is not None:
            self.add_tabu(center)
            self.trace.append((center, next_center))
            self.output.debug(4, 0, '[TABU] step forward: <%s> -> <%s>' % (center, next_center))  # debug
            self.output.debug(4, 0, '[TABU] trace length: %d' % len(self.trace))  # debug
            return visited_points

        center, next_center = self.trace.pop()
        self.remove_tabu(center)
        self.add_tabu(next_center)
        self.output.debug(4, 0, '[TABU] step backward: <%s> -> <%s>' % (next_center, center))  # debug
        self.output.debug(4, 0, '[TABU] trace length: %d' % len(self.trace))  # debug
        return visited_points + [center]

    def postprocess(self, solution: Vector):
        pass

    def is_tabu(self, point):
        return str(point.backdoor) in self.tabu

    def add_tabu(self, point):
        self.tabu.add(str(point.backdoor))
        self.output.debug(4, 0, '[TABU] add tabu: <%s>' % point)  # debug

    def remove_tabu(self, point):
        self.tabu.remove(str(point.backdoor))
        self.output.debug(4, 0, '[TABU] remove tabu: <%s>' % point)  # debug

    def neighbourhood(self, point):
        order = range(point.backdoor.length)

        if self.shuffling:
            order = list(order)
            shuffle(order)

        for j in order:
            mask = point.backdoor.get_mask()
            mask[j] = not mask[j]
            yield Point(point.backdoor.get_copy(mask))

    def _process_iteration_result(self, number, vector):
        self.output.log({
            'iteration': number,
            'spent_time': self.limit.get('time'),
            'points': [point.to_dict() for point in vector]
        })

    def __info__(self):
        return {
            **super().__info__(),
            'shuffling': self.shuffling
        }
