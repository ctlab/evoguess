from os import getpid
from typing import Iterable
from time import time as now
from pysat.solvers import Glucose3
from numpy.random import RandomState

from ..models import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status
from ..abc.function import Function, aggregate_results

from instance import Instance
from instance.module.variables import Backdoor
from instance.module.variables.vars import Supplements


def ibs_supplements(args: WorkerArgs, instance: Instance,
                    backdoor: Backdoor) -> Iterable[Supplements]:
    # IBS function works only with input dependent formulas
    if not instance.input_dependent:
        return ()

    sample_seed, _, offset, length = args
    sample_state = RandomState(sample_seed)
    encoding_data = instance.encoding.get_data()
    instance_vars = instance.get_instance_vars(backdoor)
    # todo: use solver.DEFAULT instead of Glucose3
    # todo: improve function package typing
    with Glucose3(encoding_data.clauses()) as solver:
        for index in range(offset + length):
            assumptions, _ = instance_vars.get_propagation(sample_state)
            if index >= offset:
                yield instance_vars.get_dependent(solver.propagate(assumptions)[1])


def ibs_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    for supplements in ibs_supplements(args, instance, backdoor):
        time, value, status, _ = solver.solve(
            encoding_data, measure, supplements, add_model=False
        )
        times[status.value] = times.get(status.value, 0.) + time
        values[status.value] = values.get(status.value, 0.) + value
        statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args


class InverseBackdoorSets(Function):
    slug = 'function:ibs'
    supbs_required = True

    def get_worker_fn(self) -> WorkerCallable:
        return ibs_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        times, values, statuses, count, ptime = aggregate_results(results)
        time_sum, value_sum = sum(times.values()), sum(values.values())
        power, budget, value = backdoor.power(), self.measure.budget, float('inf')

        if statuses.get(Status.RESOLVED, 0) > 0:
            value = power * budget * (3. * count / statuses[Status.RESOLVED])

        return {
            'count': count,
            'value': round(value, 2),
            'ptime': round(ptime, 4),
            'statuses': statuses,
            'time_sum': round(time_sum, 4),
            'value_sum': round(value_sum, 4),
        }


__all__ = [
    'InverseBackdoorSets',
    # utils
    'ibs_supplements'
]
