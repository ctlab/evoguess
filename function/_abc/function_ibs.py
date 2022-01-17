from .function import *


def ibs_function(tasks: Tasks, payload: Payload) -> Results:
    instance, solver, measure, _bytes = payload
    backdoor = Backdoor.unpack(_bytes)

    return []


class InverseBackdoorSets(Function):
    slug = 'function:ibs'
    name = 'Function: Inverse Backdoor Sets'

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        pass

    def get_function(self) -> WorkerCallable:
        return ibs_function


__all__ = [
    'InverseBackdoorSets',
]
