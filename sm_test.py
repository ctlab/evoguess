import json

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
FUNC_SLUG = 'function:upgad'

BD_FILE = 'backdoors'


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
    with open(f'{BD_FILE}_all', 'a+') as handle:
        handle.write(f'{key}: {json.dumps(estimation)}\n')


def log_progress(current, count, index):
    with open(f'{BD_FILE}_%', 'a+') as handle:
        handle.write(f'progress: {current}/{count} of {index}\n')


def log_len_estimation(bd_len, bd_estimations):
    with open(f'{BD_FILE}_{bd_len}', 'a+') as handle:
        for bd, est in bd_estimations:
            handle.write(f'{repr(bd)}: {json.dumps(est)}\n')


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
                'slug': 'shaping:chunks',
                'chunk_rate': CHUNK_RATE
            },
        },
        'backdoor': {
            'slug': 'backdoor:base',
        }
    })
    pargs = json.loads(args)

    _, method = build(
        {Method: [
            Function,
            Executor
        ]}, **pargs
    )

    print(WORKERS, CHUNK_RATE)
    print(COUNT, FUNC_SLUG)

    backdoor_strings = []
    with open(BD_FILE, 'r') as handle:
        for line in handle.readlines():
            backdoor_strings.append(line.strip())

    index = 0
    bd_futures = []
    estimations = {}
    instance = Instance(pargs['instance'])

    while index < len(backdoor_strings):
        if len(bd_futures) < 1000:
            bd_str = backdoor_strings[index]
            backdoor = instance.get_backdoor(**pargs['backdoor'], _list=bd_str)
            if len(backdoor) <= 11:
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

    len_index = []
    estimations_by_len = {}
    for key, bd_estimation in estimations.items():
        backdoor, _ = bd_estimation
        if len(backdoor) in estimations_by_len:
            estimations_by_len[len(backdoor)].append(bd_estimation)
        else:
            len_index.append(len(backdoor))
            estimations_by_len[len(backdoor)] = [bd_estimation]

    for bd_len in sorted(len_index):
        bd_estimations = sorted(estimations_by_len[bd_len], key=lambda x: x[1]['statistic']['false'])
        print(f'\n{bd_len}-len backdoors:')
        for backdoor, estimation in bd_estimations[:10]:
            print(f'{repr(backdoor)}: {json.dumps(estimation)}')

        log_len_estimation(bd_len, bd_estimations)
