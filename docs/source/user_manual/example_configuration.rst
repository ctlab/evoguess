Example configuration
=====================

.. code-block:: none

    {
        'algorithm': {
            'awaited_count': 1,
            'size': 8, 'elites': 2,
            'slug': 'genetic:elitism',
            'limit': {
                'value': '12:00:00',
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
            'path': 'test/pvs_7_4',
        },
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
                'count': 100
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
            'max_n': 30
        },
        'executor': {
            'workers': 4,
            'slug': 'executor:process',
            'shaping': {
                'slug': 'shaping:chunks',
                'chunk_rate': 4
            },
        },
        'backdoors': [
            {
                'slug': 'backdoor:base',
                # "_list": []
            }
        ],
    }
