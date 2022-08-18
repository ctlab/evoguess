from function.impl.function_gad import *


def rho_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    solver, measure, instance, _bytes = payload
    sample_seed, sample_size, offset, length = args
    timestamp, backdoor = now(), Backdoor.unpack()

    with solver.prototype(instance) as i_solver:
        # use incremental
        pass

    times, values, statuses = {}, {}, {}
    return times, values, statuses, args, getpid(), timestamp - now()


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'

    def get_worker_fn(self) -> WorkerCallable:
        return rho_worker_fn


__all__ = [
    'RhoFunction',
    *typings.__all__,
]
