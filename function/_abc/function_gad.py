from .function import *


def gad_function(tasks: Tasks, payload: Payload) -> Results:
    instance, solver, measure, _bytes = payload
    backdoor = Backdoor.unpack(_bytes)

    return []


class GuessAndDetermine(Function):
    slug = 'function:gad'
    name = 'Function: Guess-and-Determine'

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        pass

    def get_function(self) -> WorkerCallable:
        return gad_function


__all__ = [
    'GuessAndDetermine'
]
