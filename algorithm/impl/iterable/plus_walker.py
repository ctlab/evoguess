from ..._abc.algorithm_abc import *


class PlusWalker(AsyncAlg):
    slug = 'iterable:plus-walker'
    name = 'Algorithm(Iterable): (1+1) Walker'

    def __init__(self, mutation, selection, t, q, r, *args, **kwargs):
        self.mutation = mutation
        self.selection = selection
        self.min_vector_length = t
        self.max_pending_points = t
        self.t, self.q, self.r = t, q, r

        self.iteration = 0
        self.root, self.best = None, None
        self.vector, self.threads = [], []
        super().__init__(*args, **kwargs)

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        self.root = list(map(Point, backdoors))
        self.best = sorted(self.root)[0]
        return self.root

    def _distance(self, point1, point2):
        b1, b2 = point1.backdoor, point2.backdoor
        return sum(bit ^ b2._mask[i] for i, bit in enumerate(b1._mask))

    def get_next_points(self, vector: Vector, count: int) -> Vector:
        population = []
        print('govno', len(self.threads), [len(t) for t in self.threads])
        if len(self.threads) == 0:
            self.iteration += 1
            point = sorted(vector)[0]
            for i in range(self.t):
                t_point = self.mutation.mutate(point)
                t_point._payload.update({'t': i, 'q': 0})
                self.threads.append([t_point])
                population.append(t_point)
                self.vector.append(point)
        else:
            print('dis', [self._distance(self.vector[i], self.threads[i][-1]) for i in range(self.t)])
            for i, thread in enumerate(self.threads):
                if len(thread) < self.q and thread[-1].estimated:
                    if self._distance(self.vector[i], thread[-1]) > self.r:
                        point = self.vector[i]
                    else:
                        point = thread[-1]

                    t_point = self.mutation.mutate(point)
                    t_point._payload.update({'t': i, 'q': len(thread)})
                    population.append(t_point)
                    thread.append(t_point)

        return population

    def update_core_vector(self, vector: Vector, *points: Point) -> Vector:
        for t, point in [(p.get('t'), p) for p in points]:
            if self.vector[t] > point:
                d_args = (t, self.vector[t].get(), point.get())
                self.output.debug(1, 2, 'Update thread %2d: %.2f -> %.2f' % d_args)
                self.vector[t] = point

        if all([len(t) == self.q and t[-1].estimated for t in self.threads]):
            print('jopa', len(self.threads), points)
            vector = sorted(self.vector)[:1]
            self.vector, self.threads = [], []

        return vector

    def postprocess(self, solution: Vector):
        pass

    def __info__(self):
        return {
            **super().__info__(),
            't': self.t,
            'q': self.q,
            'r': self.r,
            'mutation': self.mutation.__info__(),
            'selection': self.selection.__info__()
        }


__all__ = [
    'PlusWalker'
]
