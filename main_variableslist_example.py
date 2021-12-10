import json

from util import build
from output import Output
from method import Method
from executor import Executor
from function import Function
from instance import Instance
from algorithm import Algorithm

if __name__ == '__main__':
    args = json.dumps({
        'algorithm': {
            'mu': 1, 'lmbda': 1,
            'size': 8, 'elites': 2,
            'slug': 'iterable:elitism',
            'limit': {
                'value': '1:00:00',
                'slug': 'limit:walltime',
            },
            'selection': {
                'slug': 'selection:roulette',
            },
            'mutation': {
                'slug': 'mutation:doer'
            },
            'crossover': {
                'slug': 'crossover:two-point'
            }
        },
        'output': {
            'slug': 'output:json',
            'path': 'test/s-n-b_6_28.cnf',
        },
        'instance': {
            'slug': 'instance',
            'cnf': {
                'slug': 'cnf',
                'path': 'snb/s-n-b_6_28.cnf'
            },
            'input_set': {
                'slug': 'variables:list',
                '_list': [169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187,
                          188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206,
                          207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225,
                          226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244,
                          245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263,
                          264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282,
                          283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301,
                          302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320,
                          321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 2399, 2400, 2401, 2402, 2403, 2404, 2405,
                          2406, 2407, 2408, 2409, 2410, 2411, 2412, 2413, 2414, 2415, 2416, 2417, 2418, 2419, 2420,
                          2421, 2422, 2423, 2424, 2425, 2426, 2427, 2428, 2429, 2430, 2431, 2432, 2433, 2434, 2435,
                          2436]
            }
        },
        'method': {
            'slug': 'method',
            'sampling': {
                'slug': 'sampling:up_steps',
                'min': 4000,
                'steps': 3
            },
            'observer': {
                'slug': 'observer:timeout',
            }
        },
        'function': {
            'slug': 'function:upgad',
            'solver': {
                'slug': 'solver:pysat:g3'
            },
            'measure': {
                'slug': 'measure:propagations'
            },
            'max_n': 20
        },
        'executor': {
            'workers': 2,
            'slug': 'executor:process',
            'shaping': {
                'slug': 'shaping:chunks',
                'chunk_rate': 2
            },
        },
        'backdoors': [
            {
                'slug': 'backdoor:base',
                "_list": []
            }
        ],
    })
    configuration = json.loads(args)

    _, algorithm = build(
        {Algorithm: [
            Output,
            Instance,
            {Method: [
                Function,
                Executor
            ]},
        ]}, **configuration
    )

    backdoors = [
        algorithm.instance.get_backdoor(**backdoor)
        for backdoor in configuration['backdoors']
    ]
    solution = algorithm.start(*backdoors)
