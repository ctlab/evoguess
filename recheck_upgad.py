import json
import os

from util import build
from time import time as now
from method._type.handler import n_completed

from method import Method
from executor import Executor
from function import Function
from instance import Instance

WORKERS = 36
CHUNK_RATE = 1

COUNT = 65_536
BY_RESULTS = True
FUNC_SLUG = 'function:upgad'

BD_PATH = os.path.join('2021.08.08_11:40:42-2021.08.09_11:40:46', 'backdoors')


def wait(bd_futures):
    completed = n_completed([f for _, f in bd_futures], 1)

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


def log_len_estimation(bd_len, bd_estimations):
    with open(f'{BD_PATH}_{bd_len}', 'a+') as handle:
        for bd, est in bd_estimations:
            handle.write(f'{repr(bd)}: {json.dumps(est)}\n')


def log_selected(backdoor_strings):
    with open(BD_PATH.replace('backdoors', 'selected_bds'), 'a+') as handle:
        for backdoor_string in backdoor_strings:
            handle.write(f'{backdoor_string}\n')


def analyse(estimations):
    len_index = []
    estimations_by_len = {}
    for key, bd_estimation in estimations.items():
        backdoor, _ = bd_estimation
        if len(backdoor) in estimations_by_len:
            estimations_by_len[len(backdoor)].append(bd_estimation)
        else:
            len_index.append(len(backdoor))
            estimations_by_len[len(backdoor)] = [bd_estimation]

    selected_backdoors = []
    for bd_len in sorted(len_index):
        try:
            bd_estimations = sorted(estimations_by_len[bd_len], key=lambda x: x[1]['statistic'][False])
        except KeyError:
            bd_estimations = sorted(estimations_by_len[bd_len], key=lambda x: x[1]['statistic']['false'])

        print(f'\n{bd_len}-len backdoors:')
        for backdoor, estimation in bd_estimations[:10]:
            print(f'{repr(backdoor)}: {json.dumps(estimation)}')

        case_index = 0
        try:
            false_cases = bd_estimations[case_index][1]['statistic'][False]
        except KeyError:
            false_cases = bd_estimations[case_index][1]['statistic']['false']
        while false_cases < 2:
            selected_backdoors.append(repr(bd_estimations[case_index][0]))
            case_index += 1
            try:
                false_cases = bd_estimations[case_index][1]['statistic'][False]
            except KeyError:
                false_cases = bd_estimations[case_index][1]['statistic']['false']

        log_len_estimation(bd_len, bd_estimations)
    log_selected(selected_backdoors)


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
    instance = Instance(pargs['instance'])

    if BY_RESULTS:
        estimations = {}
        with open(f'{BD_PATH}_all', 'r') as handle:
            for line in handle.readlines():
                bd_str, est_str = line.strip().split(': ', 1)
                backdoor = instance.get_backdoor(**pargs['backdoor'], _list=bd_str)
                estimations[bd_str] = (backdoor, json.loads(est_str))
    else:
        _, method = build(
            {Method: [
                Function,
                Executor
            ]}, **pargs
        )

        print(WORKERS, CHUNK_RATE)
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

    analyse(estimations)
