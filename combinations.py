import json

import numpy

from uuid import uuid4
from os import makedirs
from os.path import join
from time import time as now
from itertools import combinations, product
from concurrent.futures.process import ProcessPoolExecutor

from instance import Instance
from util.const import EXPERIMENT_PATH

from function.module.solver import solvers

MAX_WORKERS = 4

BACKDOORS = [
    '46..50 101 104 105 148',
    '43 66 68 70 146..150',
    '6..10 33 37 38 40',
    '18..20 88 111..115',
    '48 91..95 131 134 135'
]

configuration = {
    'instance': {
        'slug': 'instance',
        'cnf': {
            'slug': 'cnf',
            'path': 'sgen/sgen6_900_200.cnf',
        },
        'input_set': {
            'slug': 'interval',
            'start': 1, 'length': 150
        }
    },
    'solver': 'solver:pysat:g3'
}

instance = Instance(configuration['instance'])
solver = solvers.get(configuration['solver'])()
up_solver = solvers.get(f'solver:pysat:g3')()


def decimal_to_base(number, bases):
    dvalues = []
    for base in bases[::-1]:
        number, dvalue = divmod(number, base)
        dvalues.insert(0, dvalue)
    return dvalues


def worker_func(case):
    st_stamp = now()
    tag, bd_lines = case
    backdoors = [
        instance.get_backdoor('backdoor:base', _list=bd_line)
        for bd_line in bd_lines
    ]

    info = {}
    max_literal = instance.max_literal()
    all_up_tasks, all_hard_tasks = [], []
    for backdoor in backdoors:
        up_tasks, hard_tasks = [], []
        backdoor_bases = backdoor.get_bases()
        with up_solver.prototype(instance.clauses()) as slv:
            for task_i in range(backdoor.task_count()):
                values = decimal_to_base(task_i, backdoor_bases)
                assumptions = instance.get_assumptions(backdoor, values)
                status, stats, literals = slv.propagate(assumptions)
                status = not (status and len(literals) < max_literal)
                (up_tasks if status else hard_tasks).append(assumptions)

        all_up_tasks.append(up_tasks)
        all_hard_tasks.append(hard_tasks)
        info[repr(backdoor)] = f'{len(hard_tasks)} of {backdoor.task_count()}'

    progress, time_sum, prop_sum = 0, 0., 0.
    hard_cases = numpy.prod([len(h) for h in all_hard_tasks])
    with solver.prototype(instance.clauses()) as slv:
        for up_tasks in all_up_tasks:
            for assumptions in up_tasks:
                status, stats, _ = slv.solve(assumptions)
                time_sum += stats['time']
                prop_sum += stats['propagations']

        for parts in product(*all_hard_tasks):
            assumptions = sum(parts, [])
            status, stats, _ = slv.solve(assumptions)

            progress += 1
            time_sum += stats['time']
            prop_sum += stats['propagations']
            print(f'Processed {tag}: {progress}/{hard_cases} cases of time {round(time_sum, 2)} s')

    return {
        'tag': tag,
        'info': info,
        'time': time_sum,
        'hard_cases': hard_cases,
        'propagations': prop_sum,
        'work_time': now() - st_stamp,
    }


if __name__ == '__main__':
    OUT_DIR = join(EXPERIMENT_PATH, 'combinations', f'_{uuid4().hex}')
    makedirs(OUT_DIR)

    with open(join(OUT_DIR, 'INFO'), 'w+') as handle:
        handle.write(json.dumps(configuration, indent=2))
    with open(join(OUT_DIR, 'backdoors'), 'w+') as handle:
        handle.write('\n'.join(map(str, BACKDOORS)))

    cases = []
    for L in range(1, len(BACKDOORS) + 1):
        for i, comb in enumerate(combinations(BACKDOORS, L)):
            cases.append((f'{L}-{i}', comb))

    executor = None
    workers = min(MAX_WORKERS, len(cases))
    print(f'{workers} workers for {len(cases)} combinations')
    print(f'output: {OUT_DIR}')

    if workers == 1:
        task_map = map
    else:
        executor = ProcessPoolExecutor(max_workers=workers)
        task_map = executor.map

    for result in task_map(worker_func, cases):
        with open(join(OUT_DIR, result['tag']), 'w+') as handle:
            for bd, text in result['info'].items():
                handle.write(f'backdoor {bd} has {text} hard cases\n')
            handle.write(f'time: {result["time"]}\n')
            handle.write(f'work_time: {result["work_time"]}\n')
            handle.write(f'propagations: {result["propagations"]}\n')
