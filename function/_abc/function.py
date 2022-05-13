from .. import typings
from ..typings import *

from instance.impl.instance import Instance
from function.module.solver.solver import Solver
from function.module.measure.measure import Measure
from instance.typings.variables.backdoor import Backdoor


class Function:
    slug = 'function'
    name = 'Function'
    supbs_required = False

    def __init__(self, solver: Solver, measure: Measure, *args, **kwargs):
        self.solver = solver
        self.measure = measure

    def get_worker_fn(self) -> WorkerCallable:
        raise NotImplementedError

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        raise NotImplementedError

    def get_payload(self, instance: Instance, backdoor: Backdoor) -> Payload:
        return self.solver, self.measure, instance, backdoor.pack()

    def __str__(self):
        return self.name

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'solver': self.solver.__info__(),
            'measure': self.measure.__info__(),
        }


__all__ = [
    'typings',
    'Function',
    *typings.__all__
]
