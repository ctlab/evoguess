import json
import os

from method._type.futures import first_completed
from util import build
from time import time as now

from method import Method
from executor import Executor
from function import Function
from instance import Instance

WORKERS = 36
CHUNK_RATE = 1

COUNT = 65_536
BY_RESULTS = False
FUNC_SLUG = 'function:incrgad'

BD_PATH = os.path.join('2021.08.08_11:40:42-2021.08.09_11:40:46', 'selected_incr_bds')


def wait(bd_futures):
    completed = first_completed([f for _, f in bd_futures])

    next_bd_futures, done_estimations = [], []
    for bd, future in bd_futures:
        if future not in completed:
            next_bd_futures.append((bd, future))
        else:
            done_estimations.append((bd, future.result()))

    return next_bd_futures, done_estimations


def log_estimation(key, estimation):
    with open(f'{BD_PATH}_all', 'a+') as handle:
        handle.write(f'{key}: {json.dumps(estimation)}\n')


def log_progress(current, count, index):
    with open(f'{BD_PATH}_%', 'a+') as handle:
        handle.write(f'progress: {current}/{count} of {index}\n')


if __name__ == '__main__':
    args = json.dumps({
        'instance': {
            'slug': 'instance',
            'cnf': {
                'slug': 'cnf',
                'path': 'sorting/pancake_vs_selection/pancake_vs_selection_7_4.cnf'
            },
            'supbs': {
                'slug': 'interval',
                'start': 1, 'length': 28
            },
            'input_set': {
                'slug': 'interval',
                'start': 1, 'length': 3244
            }
        },
        'method': {
            'slug': 'method',
            'sampling': {
                'slug': 'sampling:const',
                'order': 'reversed',
                'count': COUNT
            },
            'observer': {
                'slug': 'observer:timeout'
            }
        },
        'function': {
            'slug': FUNC_SLUG,
            'solver': {
                'slug': 'solver:pysat:g3'
            },
            'measure': {
                'slug': 'measure:propagations'
            },
            'max_n': 20
        },
        'executor': {
            'workers': WORKERS,
            'slug': 'executor:process',
            'shaping': {
                'slug': 'shaping:single',
            },
        },
        'backdoor': {
            'slug': 'backdoor:base',
        }
    })
    pargs = json.loads(args)
    instance = Instance(pargs['instance'])

    if BY_RESULTS:
        estimations = []
        with open(f'{BD_PATH}_all', 'r') as handle:
            for line in handle.readlines():
                bd_str, est_str = line.strip().split(': ', 1)
                backdoor = instance.get_backdoor(**pargs['backdoor'], _list=bd_str)
                estimations.append((backdoor, json.loads(est_str)))

        bd_estimations = sorted(estimations, key=lambda x: x[1]['job_time'])
        for backdoor, estimation in bd_estimations[:10]:
            print(f'{repr(backdoor)}: {json.dumps(estimation)}')
    else:
        _, method = build(
            {Method: [
                Function,
                Executor
            ]}, **pargs
        )

        print(WORKERS)
        print(COUNT, FUNC_SLUG)

        backdoor_strings = []
        with open(BD_PATH, 'r') as handle:
            for line in handle.readlines():
                backdoor_strings.append(line.strip())

        index = 0
        bd_futures = []
        estimations = {}

        while index < len(backdoor_strings):
            if len(bd_futures) < 100:
                bd_str = backdoor_strings[index]
                backdoor = instance.get_backdoor(**pargs['backdoor'], _list=bd_str)
                bd_futures.append((backdoor, method.queue(instance, backdoor)))
                index += 1
            else:
                bd_futures, done = wait(bd_futures)
                for backdoor, estimation in done:
                    key = repr(backdoor)
                    log_estimation(key, estimation)
                    estimations[key] = (backdoor, estimation)
                    log_progress(len(estimations), len(backdoor_strings), index)

        while len(bd_futures) > 0:
            bd_futures, done = wait(bd_futures)
            for backdoor, estimation in done:
                key = repr(backdoor)
                log_estimation(key, estimation)
                estimations[key] = (backdoor, estimation)
                log_progress(len(estimations), len(backdoor_strings), len(backdoor_strings))
