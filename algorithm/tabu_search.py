from .algorithm import *

from random import shuffle


class TabuSearch(Algorithm):
    population_size = None
    name = 'Algorithm: Tabu Search'

    def __init__(self,
                 *args, **kwargs
                 ):
        self.trace = []
        self.tabu = set()
        self.shuffling = kwargs.get('shuffling', False)
        super().__init__(*args, **kwargs)

    def initialize(self, backdoor: Backdoor) -> Population:
        root = Individual(backdoor)
        _, estimation = self.method.queue(backdoor)
        if estimation is None:
            _, estimations = self.method.wait()  # ignore=True)
            estimation = list(estimations)[0]
            assert backdoor == estimation[0]
            estimation = estimation[1]

        best = root.set(**estimation)
        return [best]

    def iteration(self, population: Population) -> Population:
        center, next_center = population[-1], None

        visited_points = []
        for point in self.neighbourhood(center):
            if self.is_tabu(point):
                continue

            backdoor = point.backdoor
            job_id, estimation = self.method.queue(backdoor)
            if estimation is None:
                estimations = []
                while len(estimations) == 0:
                    _, estimations = self.method.wait()  # ignore=True)

                bd, estimation = list(estimations)[0]
                assert str(bd) == str(backdoor)

            point.set(**estimation)
            visited_points.append(point)
            if center > point:
                next_center = point
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

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    def is_tabu(self, point):
        return str(point.backdoor) in self.tabu

    def add_tabu(self, point):
        self.tabu.add(str(point.backdoor))
        self.output.debug(4, 0, '[TABU] add tabu: <%s>' % point)  # debug

    def remove_tabu(self, point):
        self.tabu.remove(str(point.backdoor))
        self.output.debug(4, 0, '[TABU] remove tabu: <%s>' % point)  # debug

    def neighbourhood(self, i):
        order = range(i.backdoor.length)

        if self.shuffling:
            order = list(order)
            shuffle(order)

        for j in order:
            v = i.backdoor.get_mask()
            v[j] = not v[j]
            yield Individual(i.backdoor.get_copy(v))

    @staticmethod
    def parse(params):
        return {} if params == "!" else None

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            'Shuffling: %s' % self.shuffling,
            '--------------------',
            self.method,
        ]))


__all__ = [
    'TabuSearch',
    'Population'
]
