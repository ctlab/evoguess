import json
from os.path import join
from operator import attrgetter
from concurrent.futures.process import ProcessPoolExecutor

from instance import Instance
from util.const import EXPERIMENT_PATH
from function.module.solver import solvers

MAX_WORKERS = 36
MAX_COUNT = 65_536

SOLVER = 'g3'
PROJECT = 'aaai_2021'
TARGET_FILE = 'BEST'

# INSTANCE, EXPERIMENT = 'pvs_4_7_simp', '2021.08.25_22:13:53-2021.08.26_10:13:54'  # 2/8 n20 2k 12h async $
# INSTANCE, EXPERIMENT = 'pvs_4_7_simp', '2021.08.25_22:13:54-2021.08.26_10:13:54'  # 2/8 n20 1k 12h async $
# INSTANCE, EXPERIMENT = 'pvs_4_7_simp', '2021.08.26_20:46:54-2021.08.27_08:46:55'  # 2/8 n20 1k 12h iter
# INSTANCE, EXPERIMENT = 'pvs_4_7_simp', '2021.08.26_20:46:57-2021.08.27_08:46:57'  # 2/8 n20 4k 12h iter
# INSTANCE, EXPERIMENT = 'pvs_4_7_simp', '2021.08.26_20:46:58-2021.08.27_08:46:58'  # 2/8 n20 2k 12h iter
INSTANCE, EXPERIMENT = 'pvs_5_7_simp', '2021.08.30_05:51:03-2021.08.30_17:51:03'  # 2/8 n20 2k 12h iter []

# INSTANCE, EXPERIMENT = 'bvp_4_8_simp', '2021.08.30_05:51:01-2021.08.30_17:51:02'  # 2/8 n20 2k 12h iter []
# INSTANCE, EXPERIMENT = 'bvp_6_7_simp', '2021.08.30_05:41:00-2021.08.30_17:41:00'  # 2/8 n20 2k 12h iter []

# INSTANCE, EXPERIMENT = 'bvs_4_8_simp', '2021.08.29_23:49:05-2021.08.30_11:49:05'  # 2/8 n20 2k 12h iter []
# INSTANCE, EXPERIMENT = 'bvs_6_7_simp', '2021.08.30_05:40:02-2021.08.30_17:40:02'  # 2/8 n20 2k 12h iter []

instances = {
    'pvs_4_7_simp': {
        'input': 1213, 'tags': ['pancake_vs_selection', '4x7_simp'],
        'path': 'sorting/pancake_vs_selection/pancake_vs_selection_7_4_simp.cnf'
    },
    'pvs_5_7_simp': {
        'input': 1596, 'tags': ['pancake_vs_selection', '5x7_simp'],
        'path': 'sorting/pancake_vs_selection/pancake_vs_selection_7_5_simp.cnf'
    },
    #
    # bubble_vs_pancake
    #
    'bvp_4_8_simp': {
        'input': 1315, 'tags': ['bubble_vs_pancake', '4x8_simp'],
        'path': 'sorting/bubble_vs_pancake/bubble_vs_pancake_8_4_simp.cnf'
    },  # 6100
    'bvp_6_7_simp': {
        'input': 1558, 'tags': ['bubble_vs_pancake', '6x7_simp'],
        'path': 'sorting/bubble_vs_pancake/bubble_vs_pancake_7_6_simp.cnf'
    },  # 2300
    #
    # bubble_vs_selection
    #
    'bvs_4_8_simp': {
        'input': 1314, 'tags': ['bubble_vs_selection', '4x8_simp'],
        'path': 'sorting/bubble_vs_selection/bubble_vs_selection_8_4_simp.cnf'
    },  # 2500
    'bvs_6_7_simp': {
        'input': 1531, 'tags': ['bubble_vs_selection', '6x7_simp'],
        'path': 'sorting/bubble_vs_selection/bubble_vs_selection_7_6_simp.cnf'
    },  # 1700
}

# use custom path to file with backdoors
# BD_PATH = ''
# or use backdoors file from experimental folder
BD_PATH = join(EXPERIMENT_PATH, PROJECT, *instances[INSTANCE]['tags'], EXPERIMENT, TARGET_FILE)


def decimal_to_base(number, bases):
    dvalues = []
    for base in bases[::-1]:
        number, dvalue = divmod(number, base)
        dvalues.insert(0, dvalue)
    return dvalues


def worker_func(bd_line):
    backdoor = instance.get_backdoor('backdoor:base', _list=bd_line)
    if backdoor.task_count() > MAX_COUNT:
        return {'backdoor': bd_line, 'time': float('inf'), 'propagations': float('inf')}

    up_tasks, hard_tasks = [], []
    max_literal = instance.max_literal()
    backdoor_bases = backdoor.get_bases()
    with solver.prototype(instance.clauses()) as slv:
        for task_i in range(backdoor.task_count()):
            values = decimal_to_base(task_i, backdoor_bases)
            assumptions = instance.get_assumptions(backdoor, values)
            status, stats, literals = slv.propagate(assumptions)
            status = not (status and len(literals) < max_literal)
            (up_tasks if status else hard_tasks).append((task_i, assumptions))

    all_tasks = up_tasks + hard_tasks
    progress, time_sum, prop_sum = 0, 0., 0.
    statistic = {'up': len(up_tasks), 'hard': len(hard_tasks)}
    with solver.prototype(instance.clauses()) as slv:
        for task_i, assumptions in all_tasks:
            status, stats, _ = slv.solve(assumptions)

            progress += 1
            time_sum += stats['time']
            prop_sum += stats['propagations']
            print(f'solved {progress}/{len(all_tasks)}, spent {round(time_sum, 2)} sec')

    return {
        'time': time_sum,
        'backdoor': bd_line,
        'statistic': statistic,
        'propagations': prop_sum
    }


if __name__ == '__main__':
    instance = Instance({
        'slug': 'instance',
        'cnf': {
            'slug': 'cnf',
            'path': instances[INSTANCE]['path']
        },
        'input_set': {
            'slug': 'interval',
            'start': 1, 'length': instances[INSTANCE]['input']
        }
    })
    solver = solvers.get(f'solver:pysat:{SOLVER}')()

    backdoor_lines = []
    with open(BD_PATH, 'r') as handle:
        for line in handle.readlines():
            backdoor_lines.append(line.strip())

    executor = None
    workers = min(MAX_WORKERS, len(backdoor_lines))
    print(f'{workers} workers for {len(backdoor_lines)} backdoors')

    if workers == 1:
        task_map = map
    else:
        executor = ProcessPoolExecutor(max_workers=workers)
        task_map = executor.map

    all_results = []
    for result in task_map(worker_func, backdoor_lines):
        all_results.append(result)
        with open(f'{BD_PATH}_{SOLVER}_VALUES', 'a+') as handle:
            handle.write(f'{json.dumps(result)}\n')

    if len(backdoor_lines) > 1:
        time_results = sorted(all_results, key=lambda x: x['time'])
        with open(f'{BD_PATH}_{SOLVER}_BY_TIME', 'w+') as handle:
            for time_result in time_results:
                handle.write(f'{json.dumps(time_result)}\n')

        prop_results = sorted(all_results, key=lambda x: x['propagations'])
        with open(f'{BD_PATH}_{SOLVER}_BY_PROPS', 'w+') as handle:
            for prop_result in prop_results:
                handle.write(f'{json.dumps(prop_result)}\n')
