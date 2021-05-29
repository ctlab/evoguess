from util.array import concat
from .._abc.function import *

from os import getpid
from time import time as now
from multiprocessing.managers import SharedMemoryManager

managers = {

}


def sgad_function(i, solver, instance, data, key=None):
    st_timestamp = now()
    bd_vars, all_values, ad_values = data
    simple_bd = list(bd_vars), []
    values = [all_values[i * len(simple_bd) + j] for j in range(len(bd_vars))]
    assumptions = instance.get_assumptions(simple_bd, values, to_base=False)

    status, stats, _ = solver.solve(instance.clauses(), assumptions, key=key)
    result = (i, getpid(), status, stats, (st_timestamp, now()))
    # todo: reformat results
    return result
    # return destruct_result(result)


class SharedGuessAndDetermine(Function):
    type = 'gad'
    slug = 'function:sgad'
    name = 'Function: Shared Guess-and-Determine'

    def get_function(self):
        return sgad_function

    def prepare_tasks(self, instance, backdoor, *dimension, **kwargs):
        tasks, ad_bits = [], []
        smm = SharedMemoryManager()
        smm.start()
        managers[str(backdoor)] = smm

        def dim_gen():
            for values in dimension:
                for value in values:
                    yield int(value)

        all_dim = list(dim_gen())
        print(len(all_dim))

        bits = smm.ShareableList(all_dim)
        ad_bits = smm.ShareableList(ad_bits)
        bd_vars = smm.ShareableList(backdoor.snapshot())
        for i in range(len(dimension)):
            tasks.append((i, self.solver, instance, [bd_vars, bits, ad_bits]))
        return tasks

    def calculate(self, backdoor, *cases):
        statistic = {True: 0, False: 0, None: 0}
        process_time, time_sum, value_sum = 0, 0, 0
        for case in cases:
            statistic[case[2]] += 1
            time_sum += case[3]['time']
            value_sum += self.measure.get(case[3])
            process_time += case[4][1] - case[4][0]

        time, value, = None, None
        count = backdoor.task_count()
        if count == len(cases):
            time, value = time_sum, value_sum
        elif len(cases) > 0:
            time = float(time_sum) / len(cases) * count
            value = float(value_sum) / len(cases) * count

        return {
            'time': time,
            'value': value,
            'count': len(cases),
            'job_time': time_sum,
            'process_time': process_time,
            'statistic': statistic
        }


__all__ = [
    'SharedGuessAndDetermine'
]
