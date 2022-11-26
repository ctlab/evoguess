from os import getpid
from time import time as now

from ..abc.function import aggregate_results
from ..models import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from .function_gad import GuessAndDetermine, gad_supplements

from function.module.solver import Solver
from function.module.measure import Measure
from instance.module.variables import Backdoor


def rho_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for assumptions, _ in gad_supplements(args, instance, backdoor):
            # todo: use constraints with incremental propagation?
            time, value, status, _ = incremental.propagate(assumptions)

            times[status.value] = times.get(status.value, 0.) + time
            values[status.value] = values.get(status.value, 0.) + value
            statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args


class RhoFunction(GuessAndDetermine):
    slug = 'function:rho'

    def __init__(self, solver: Solver, measure: Measure,
                 penalty_power: float = 0.):
        super().__init__(solver, measure)
        self.penalty_power = penalty_power

    def get_worker_fn(self) -> WorkerCallable:
        return rho_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        times, values, statuses, count, ptime = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        bases, value = backdoor.get_var_bases(), value_sum if count else None

        # todo: implement rho calculate function
        raise NotImplementedError
        # if count > 0 and count != power:
        #     propagated = float(statuses[Status.RESOLVED]) / count
        #     # try avoid overflow exception
        #     if 0 < self.penalty_power < power:
        #         power_scale = power / self.penalty_power
        #
        #     value = log2(propagated / count * power + (1. - propagated / count) * penalty_power)

        # return {
        #     'count': count,
        #     'ptime': round(ptime, 4),
        #     'value': round(value, 6),
        #     'statuses': statuses,
        #     'time_sum': round(time_sum, 4),
        #     'value_sum': round(value_sum, 4),
        # }


__all__ = [
    'RhoFunction'
]
