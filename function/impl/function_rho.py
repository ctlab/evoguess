from function.impl.function_gad import *

from os import getpid
from time import time as now


def rho_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    preset = solver.preset(instance.encoding, measure)
    for supplements in gad_supplements(args, instance, backdoor):
        # todo: use incremental propagation!!
        time, status, value, _ = preset.propagate(supplements, add_model=False)

        times[status] = times.get(status, 0.) + time
        values[status] = values.get(status, 0.) + value
        statuses[status] = statuses.get(status, 0) + 1
    # todo: (optimize) dumps dict to str?
    return getpid(), now() - timestamp, times, values, statuses, args


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'

    def get_worker_fn(self) -> WorkerCallable:
        return rho_worker_fn


__all__ = [
    'RhoFunction'
]
