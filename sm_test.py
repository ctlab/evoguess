import json

from util import build
from time import time as now

from instance._type.variables import BaseBackdoor

from method import Method
from executor import Executor
from function import Function
from instance import Instance

WORKERS = 4
CHUNK_RATE = 4

COUNT = 10_000
FUNC_SLUG = 'function:gad'
# ------ | gad  | sgad
# ---------------------
#   1000 |      |
# ---------------------
#   5000 |      |
# ---------------------
#  10000 |      |
# ---------------------
#  20000 | 123  | 106
# ---------------------
#  50000 | 250  | 260
# ---------------------
# 100000 |  499 | 511


if __name__ == '__main__':
    args = json.dumps({
        'instance': {
            'slug': 'instance',
            'cnf': {
                'slug': 'cnf',
                'path': '/Users/alpha/evoguess/evoguess_data/templates/sorting/pancake_vs_selection/pancake_vs_selection_7_4.cnf'
            },
            'secret_key': {
                'slug': 'interval',
                'start': 1, 'length': 28
            }
        },
        'method': {
            'slug': 'method',
            'seed': 323232,
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
                'slug': 'measure:time'
            }
        },
        'executor': {
            'workers': WORKERS,
            'slug': 'executor:process',
            'shaping': {
                'slug': 'shaping:chunks',
                'chunk_rate': CHUNK_RATE
            },
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

    instance = Instance(pargs['instance'])
    backdoor = BaseBackdoor(2, instance.secret_key)

    timestamp = now()
    future = method.queue(instance, backdoor)
    estimation = future.result()
    print(estimation)

    print('time: ', now() - timestamp)
