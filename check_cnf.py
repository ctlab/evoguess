import json
from concurrent.futures.process import ProcessPoolExecutor

from instance import Instance
from function.module.solver import solvers

MAX_WORKERS = 36

SOLVERS = ['g3', 'g4', 'cd']
INSTANCES = {
    'sgen_150_100': 'sgen/sgen6_900_100.cnf',
    'sgen_150_200': 'sgen/sgen6_900_200.cnf',
    'sgen_150_300': 'sgen/sgen6_900_300.cnf',
    'sgen_150_1001': 'sgen/sgen6_900_1001.cnf',
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
