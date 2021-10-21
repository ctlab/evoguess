import subprocess
from os import makedirs

from numpy.random import RandomState

from instance import Instance
from function.module.solver import solvers
from util.const import TEMPLATE_PATH

instance = Instance({
    'slug': 'instance',
    'cnf': {
        'slug': 'cnf',
        'path': 'a5_1.cnf'
    },
    'input_set': {
        'slug': 'interval',
        'start': 1, 'length': 64
    }
})

seed = 295
out_len = 128
simplifier_path = '~/evoguess/other/minisat/simp/minisat'

rs = RandomState(seed=seed)
sk = instance.get_backdoor('backdoor:base')
solver = solvers.get('solver:pysat:g3')()

for i in range(20):
    values = rs.randint(0, 2, size=len(sk))
    assumptions = instance.get_assumptions(sk, values)
    _, _, solution = solver.solve(instance.clauses(), assumptions)

    ks = solution[-out_len:]
    sk_bits = ''.join(map(str, values))
    makedirs(f'{TEMPLATE_PATH}/a5_1_{out_len}', exist_ok=True)
    input_cnf_simp = f'{TEMPLATE_PATH}/a5_1_{out_len}/{seed}-{sk_bits}.cnf'
    output_cnf_simp = f'{TEMPLATE_PATH}/a5_1_{out_len}/{seed}-{sk_bits}_simp.cnf'
    with open(input_cnf_simp, 'w+') as handle:
        with open(instance.cnf.path, 'r') as template:
            handle.writelines(template.readlines())

        for output_bit in ks:
            handle.write(f'{output_bit} 0\n')

    p = subprocess.Popen([simplifier_path, input_cnf_simp, f'-dimacs={output_cnf_simp}'])
    output, err = p.communicate()
    print(output, err)
