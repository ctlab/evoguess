from ..streaming_alg import *

Individual = Point
Population = Vector


class Evolution(StreamingAlg):
    min_tweak_size = 1
    population_size = None
    name = 'Algorithm(Streaming): Evolution'

    def __init__(self, mutation, selection, *args, **kwargs):
        self.mutation = mutation
        self.selection = selection
        self.stagnation = kwargs.get("stagnation", 0)
        self.in_process_count = self.population_size

        self.root, self.best = None, None
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    def preprocess(self, *backdoors: Backdoor) -> Vector:
        self.root = list(map(Individual, backdoors))
        self.best = sorted(self.root)[0]
        self.limit.set('stagnation', 0)
        return self.root

    def get_next_points(self, vector: Population, count: int) -> Individual:
        # todo: consider stagnation
        size = max(count, self.min_tweak_size)
        selected = self.selection.breed(vector, size)
        return self.tweak(selected)

    def update_core_vector(self, vector: Population, *points: Individual) -> Population:
        population = self.join(vector, points)
        self._update_best(population)
        return population

    def postprocess(self, solution: Population):
        pass

    def _update_best(self, population):
        population_best = sorted(population)[0]
        if self.best > population_best:
            self.limit.increase('stagnation')
        else:
            self.best = population_best
            self.limit.set('stagnation', 0)

    def __info__(self):
        return {
            **super().__info__(),
            'stagnation': self.stagnation,
            'mutation': self.mutation.__info__(),
            'selection': self.selection.__info__()
        }


__all__ = [
    'Evolution',
    'Individual',
    'Population',
]
