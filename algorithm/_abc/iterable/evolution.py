from ..iterable_alg import *

Individual = Point
Population = Vector


class Evolution(IterableAlg):
    population_size = None
    name = 'Algorithm(Iterable): Evolution'

    def __init__(self, mutation, selection, *args, **kwargs):
        self.mutation = mutation
        self.selection = selection
        self.vector_length = self.population_size
        self.stagnation = kwargs.get("stagnation", 0)

        self.root, self.best = None, None
        super().__init__(*args, **kwargs)

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    def preprocess(self, *backdoors: Backdoor) -> Population:
        self.root = list(map(Individual, backdoors))
        self.best = sorted(self.root)[0]
        self.limit.set('stagnation', 0)
        return self.root

    def start_iteration(self, vector: Vector) -> Vector:
        selected = self.selection.breed(vector, self.population_size)
        return self.tweak(selected)

    def end_iteration(self, parents: Vector, child: Vector) -> Vector:
        population = self.join(parents, child)
        if self._is_stagnation(population):
            population = [self.root]
        return population

    def postprocess(self, solution: Population):
        pass

    def _is_stagnation(self, population):
        population_best = sorted(population)[0]
        if population_best > self.best:
            stagnation = self.limit.increase('stagnation')
        else:
            self.best = population_best
            stagnation = self.limit.set('stagnation', 0)

        return self.stagnation and stagnation > self.stagnation

    def __info__(self):
        return {
            **super().__info__(),
            'stagnation': self.stagnation,
            'mutation': self.mutation.__info__(),
            'selection': self.selection.__info__()
        }


__all__ = [
    'Evolution',
    'Population'
]
