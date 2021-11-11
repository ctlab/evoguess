from ..._abc.algorithm_iterable import *

from numpy.random import randint, RandomState


class TabuSearch(AlgorithmIterable):
    slug = 'iterable:tabu_search'
    name = 'Algorithm(Iterable): Tabu Search'

    def __init__(self, *args, **kwargs):
        self.trace, self.tabu = [], set()
        super().__init__(*args, **kwargs)

        self.shuffle_seed = kwargs.get('shuffle_seed', randint(2 ** 32 - 1))
        self.shuffle_state = RandomState(seed=self.shuffle_seed)

    def iteration(self, vector: Vector) -> Vector:
        visited_points = []
        center, next_center = vector[-1], None
        for point in self.neighbourhood(center):
            if self.is_tabu(point):
                continue

            estimated, _ = self._await(self._queue(point), count=1)
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

    def is_tabu(self, point):
        return str(point.backdoor) in self.tabu

    def add_tabu(self, point):
        self.tabu.add(str(point.backdoor))
        self.output.debug(4, 0, '[TABU] add tabu: <%s>' % point)  # debug

    def remove_tabu(self, point):
        self.tabu.remove(str(point.backdoor))
        self.output.debug(4, 0, '[TABU] remove tabu: <%s>' % point)  # debug

    def neighbourhood(self, point):
        size = point.backdoor.length
        for index in self.shuffle_state.permutation(size):
            mask = point.backdoor.get_mask()
            mask[index] = not mask[index]
            yield Point(point.backdoor.get_copy(mask))

    def __info__(self):
        return {
            **super().__info__(),
            'shuffle_seed': self.shuffle_seed
        }


__all__ = [
    'TabuSearch'
]
