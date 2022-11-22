from os import getpid
from time import time as now

from ..abc.function import aggregate_results
from ..typings import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation
from .function_gad import GuessAndDetermine, gad_supplements

from instance.module.variables import Backdoor


def rho_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for assumptions, _ in gad_supplements(args, instance, backdoor):
            # todo: use constraints with incremental propagation?
            time, status, value, _ = incremental.propagate(assumptions)

            times[status] = times.get(status, 0.) + time
            values[status] = values.get(status, 0.) + value
            statuses[status] = statuses.get(status, 0) + 1
    # todo: (optimize) dumps dict to str?
    return getpid(), now() - timestamp, times, values, statuses, args


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'

    def get_worker_fn(self) -> WorkerCallable:
        return rho_worker_fn

    # def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
    #     times, values, statuses, count = aggregate_results(results)
    #     time_sum, value_sum = sum(times.values()), sum(values.values())
    #     power, value = backdoor.power(), value_sum if count else None
    #
    #     # todo: add RhoFunction.calculate realisation!
    #     raise NotImplementedError

        # return {
        #     'value': value,
        #     'count': count,
        #     'statuses': statuses,
        #     'time_sum': round(time_sum, 4),
        #     'value_sum': round(value_sum, 4),
        # }


__all__ = [
    'RhoFunction'
]
