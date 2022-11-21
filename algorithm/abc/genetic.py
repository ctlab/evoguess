from typing import List, Iterable, Tuple

from .evolution import Evolution
from ..module.mutation import Mutation
from ..module.selection import Selection
from ..module.crossover import Crossover

from typings.optional import Int
from core.model.point import Vector
from util.iterable import slice_by, concat
from instance.module.variables import Backdoor


class Genetic(Evolution):
    tweak_size = 2

    def __init__(self, min_update_size: int, max_queue_size: Int,
                 selection: Selection, mutation: Mutation, crossover: Crossover):
        super().__init__(min_update_size, max_queue_size, selection, mutation)
        self.crossover = crossover

    def join(self, parents: Vector, offspring: Vector) -> Vector:
        raise NotImplementedError

    def tweak(self, selected: List[Backdoor]) -> List[Backdoor]:
        return concat(*map(self._apply, slice_by(selected, 2)))

    def _apply(self, individuals: Tuple[Backdoor]) -> Iterable[Backdoor]:
        if len(individuals) == 2:
            individuals = self.crossover.cross(*individuals)
        return map(self.mutation.mutate, individuals)

    def __info__(self):
        return {
            **super().__info__(),
            'crossover': self.crossover
        }


__all__ = [
    'Genetic'
]
