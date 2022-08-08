import sys
import numpy
import argparse

from os import makedirs
from os.path import join
from time import time as now
from itertools import combinations, product

from instance.typings import Backdoor
from instance.module.encoding import CNF
from function.module.solver import solvers

up_solver = solvers.get(f'solver:pysat:g3')()


def decimal_to_base(number, bases):
    dvalues = []
    for base in bases[::-1]:
        number, dvalue = divmod(number, base)
        dvalues.insert(0, dvalue)
    return dvalues


def worker_func(args):
    st_stamp = now()
    case, cnf, solver, bds = args
    backdoors = list(map(Backdoor.parse, bds))

    info = {}
    max_literal = cnf.get_data().max_literal()
    all_up_tasks, all_hard_tasks = [], []
    for backdoor in backdoors:
        up_tasks, hard_tasks = [], []
        variables = backdoor.variables()
        backdoor_bases = backdoor.get_bases()
        with up_solver.prototype(cnf.get_data()) as slv:
            for task_i in range(backdoor.task_count()):
                values = decimal_to_base(task_i, backdoor_bases)

                assumptions = [x if values[i] else -x for i, x in enumerate(variables)]

                status, stats, literals = slv.propagate(assumptions)
                status = not (status and len(literals) < max_literal)
                (up_tasks if status else hard_tasks).append(assumptions)

        all_up_tasks.append(up_tasks)
        all_hard_tasks.append(hard_tasks)
        info[repr(backdoor)] = f'{len(hard_tasks)} of {backdoor.task_count()}'

    progress, time_sum, prop_sum = 0, 0., 0.
    hard_cases = numpy.prod([len(h) for h in all_hard_tasks])

    print(f'Generated {hard_cases} hard tasks')
    with solver.prototype(cnf.get_data()) as slv:
        for up_tasks in all_up_tasks:
            for assumptions in up_tasks:
                status, stats, _ = slv.solve(assumptions, expect_interrupt=False)
                time_sum += stats['time']
                prop_sum += stats['propagations']

        for parts in product(*all_hard_tasks):
            assumptions = sum(parts, [])
            status, stats, _ = slv.solve(assumptions, expect_interrupt=False)

            progress += 1
            time_sum += stats['time']
            prop_sum += stats['propagations']
            print(f'Processed {case}: {progress}/{hard_cases} cases of time {round(time_sum, 2)} s')

    return {
        'info': info,
        'time': time_sum,
        'hard_cases': hard_cases,
        'propagations': prop_sum,
        'work_time': now() - st_stamp,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EvoGuess v2 Combinations')
    parser.add_argument('-c', '--cnf', metavar='<instance file>', type=str)
    parser.add_argument('-s', '--solver', metavar='<solver key>', type=str)
    parser.add_argument('-o', '--output', metavar='<output dir>', type=str)
    parser.add_argument('-b', '--backdoors', metavar='<backdoors file>', type=str)

    args, _ = parser.parse_known_args()

    assert args.cnf, 'Specify CNF instance file'
    assert args.solver, 'Specify SAT solver key'
    assert args.backdoors, 'Specify backdoors file'

    cnf = CNF(path=args.cnf)
    solver = solvers.get(f'solver:pysat:{args.solver}')()
    out_dir = args.output or f'data/combinations/{args.cnf}'
    makedirs(out_dir, exist_ok=True)

    with open(args.backdoors, 'r') as handle:
        backdoors = [line.strip() for line in handle.readlines()]

    with open(join(out_dir, 'INFO'), 'w+') as handle:
        handle.write('python3 %s\n\n' % ' '.join(sys.argv))
        handle.write('\n'.join(map(str, backdoors)))

    for L in range(len(backdoors) + 1, 1, -1):
        for i, bds in enumerate(combinations(backdoors, L)):
            case = f'{L}-{i}'
            out_file = join(out_dir, case)

            args = (case, cnf, solver, bds)
            result = worker_func(args)

            with open(out_file, 'w+') as handle:
                for bd, text in result['info'].items():
                    handle.write(f'backdoor {bd} has {text} hard cases\n')
                handle.write(f'time: {result["time"]}\n')
                handle.write(f'work_time: {result["work_time"]}\n')
                handle.write(f'propagations: {result["propagations"]}\n')
