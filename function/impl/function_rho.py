from function.impl.function_gad import *


def rho_function(tasks: list[TaskId], payload: Payload) -> list[Result]:
    instance, solver, measure, _bytes = payload
    backdoor = Backdoor.unpack(_bytes)

    with solver.prototype(instance) as i_solver:
        # use incremental
        pass

    return []


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'
    name = 'Function: Rho'

    def get_function(self) -> WorkerCallable:
        return rho_function


__all__ = [
    'RhoFunction'
]
