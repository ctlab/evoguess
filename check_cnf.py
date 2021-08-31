import json
from concurrent.futures.process import ProcessPoolExecutor

from instance import Instance
from function.module.solver import solvers

MAX_WORKERS = 36

SOLVERS = ['g3', 'g4', 'cd']
INSTANCES = {
    'pvs_4_7': 'sorting/pancake_vs_selection/pancake_vs_selection_7_4.cnf',
    'pvs_5_7': 'sorting/pancake_vs_selection/pancake_vs_selection_7_5.cnf',
    'pvs_3_8': 'sorting/pancake_vs_selection/pancake_vs_selection_8_3.cnf',
    #
    'bvs_4_8': 'sorting/bubble_vs_selection/bubble_vs_selection_8_4.cnf',
    'bvs_5_8': 'sorting/bubble_vs_selection/bubble_vs_selection_8_5.cnf',
    'bvs_6_7': 'sorting/bubble_vs_selection/bubble_vs_selection_7_6.cnf',
    'bvs_7_7': 'sorting/bubble_vs_selection/bubble_vs_selection_7_7.cnf',
    #
    'bvp_3_8': 'sorting/bubble_vs_pancake/bubble_vs_pancake_8_3.cnf',
    'bvp_4_8': 'sorting/bubble_vs_pancake/bubble_vs_pancake_8_4.cnf',
    'bvp_5_8': 'sorting/bubble_vs_pancake/bubble_vs_pancake_8_5.cnf',
    'bvp_6_7': 'sorting/bubble_vs_pancake/bubble_vs_pancake_7_6.cnf',
    'bvp_7_7': 'sorting/bubble_vs_pancake/bubble_vs_pancake_7_7.cnf',
}


def worker_func(data):
    instance_key, solver_key = data
    clauses = Instance({
        'slug': 'instance',
        'cnf': {
            'slug': 'cnf',
            'path': INSTANCES[instance_key]
        },
        'input_set': None
    }).clauses()

    solver = solvers.get(f'solver:pysat:{solver_key}')()
    status, statistic, _ = solver.solve(clauses, [])
    return {
        'solver': solver_key,
        'instance': instance_key,
        'status': status,
        'statistic': statistic,
    }


if __name__ == '__main__':
    cases = [
        (i_key, s_key)
        for s_key in SOLVERS
        for i_key in INSTANCES.keys()
    ]
    workers = min(MAX_WORKERS, len(cases))
    print(f'{workers} workers for {len(cases)} cases')

    if workers == 1:
        task_map = map
    else:
        executor = ProcessPoolExecutor(max_workers=workers)
        task_map = executor.map

    all_results = []
    for result in task_map(worker_func, cases):
        all_results.append(result)
        with open('CNF_RESULTS', 'a+') as handle:
            handle.write(f'{json.dumps(result)}\n')
