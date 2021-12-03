from ..algorithm import *

from .mutation.mutation import Mutation
from .selection.selection import Selection


class Evolution(Algorithm):
    population_size = None
    name = 'Algorithm: Evolution'

    def __init__(self,
                 mutation: Mutation,
                 selection: Selection,
                 *args, **kwargs
                 ):
        self.mutation = mutation
        self.selection = selection
        self.stagnation = kwargs.get("stagnation", 0)
        super().__init__(*args, **kwargs)

        self.root, self.best = None, None

    def initialize(self, backdoor: Backdoor) -> Population:
        self.root = Individual(backdoor)
        _, estimation = self.method.queue(backdoor)
        if estimation is None:
            _, estimations = self.method.wait()  # ignore=True)
            estimation = list(estimations)[0]
            assert backdoor == estimation[0]
            estimation = estimation[1]

        self.limit.set('stagnation', 0)
        self.best = self.root.set(**estimation)
        return [self.best]

    def iteration(self, population: Population) -> Population:
        selected = self.selection.breed(population, self.population_size)
        children = self.tweak(selected)

        await_list = {}
        for individual in children:
            backdoor = individual.backdoor
            job_id, estimation = self.method.queue(backdoor)
            if estimation is None:
                bd_key = str(backdoor)
                if bd_key not in await_list:
                    await_list[bd_key] = []
                await_list[bd_key].append(individual)
            else:
                individual.set(**estimation)

        while len(await_list) > 0:
            _, estimations = self.method.wait()  # ignore=True)
            for backdoor, estimation in estimations:
                bd_key = str(backdoor)
                individuals = await_list.pop(bd_key)
                for individual in individuals:
                    individual.set(**estimation)

        new_population = self.join(population, children)
        if self._is_stagnation(new_population):
            new_population = [self.root]
        return new_population

    def tweak(self, selected: Population):
        raise NotImplementedError

    def join(self, parents: Population, children: Population):
        raise NotImplementedError

    def _is_stagnation(self, population):
        population_best = sorted(population)[0]
        if self.best > population_best:
            stagnation = self.limit.set('stagnation', 0)
        else:
            stagnation = self.limit.increase('stagnation')

        self.output.debug(3, 0, f'Stagnation count: {stagnation}')
        return self.stagnation and stagnation > self.stagnation

    @staticmethod
    def parse(params):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.limit,
            self.selection,
            self.mutation,
            '--------------------',
            self.method,
        ]))


__all__ = [
    'Evolution',
    'Population'
]
