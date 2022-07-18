from numpy.random import RandomState

from algorithm.impl import Elitism
from algorithm.module.limit import WallTime
from algorithm.module.evolution.mutation import Doer
from algorithm.module.evolution.crossover import TwoPoint
from algorithm.module.evolution.selection import Roulette

from method.impl import Method
from method.module.sampling import Const

from function.impl import GuessAndDetermine
from function.module.measure.impl import SolvingTime
from function.module.solver.impl.native import Cadical5

from executor.impl import MPIExecutor
from executor.module.shaping.impl import Chunks

from instance.impl import Instance
from instance.typings.cnf import CNF
from instance.typings import Variables
from instance.typings.var import Index, Merged
from instance.typings.operator import xor, majority, bent_4

from output.impl import JSONOut
from util.array import slice_by_size

SUPBS_VARS = list(range(1, 33))
RANDOM_STATE = RandomState(seed=43)

XOR_GROUPS = slice_by_size(2, SUPBS_VARS)
MAJ_GROUPS = slice_by_size(3, [*SUPBS_VARS[:30], *SUPBS_VARS[29:32]])
BENT4_GROUPS = slice_by_size(4, SUPBS_VARS)

# XOR_PERM_COUNT = 10
# XOR_PERM_LISTS = [
#     slice_by_size(2, list(RANDOM_STATE.permutation(SUPBS_VARS)))
#     for _ in range(XOR_PERM_COUNT)
# ]

MAJ_PERM_LISTS = []
MAJ_PERM_COUNT = 15
for _ in range(MAJ_PERM_COUNT):
    perm = list(RANDOM_STATE.permutation(SUPBS_VARS))
    MAJ_PERM_LISTS.append(slice_by_size(3, [*perm[:30], *perm[29:32]]))
    print(MAJ_PERM_LISTS[-1])

# BENT4_PERM_COUNT = 20
# BENT4_PERM_LISTS = [
#     slice_by_size(4, list(RANDOM_STATE.permutation(SUPBS_VARS)))
#     for _ in range(BENT4_PERM_COUNT)
# ]

algorithm = Elitism(
    size=9, elites=2,
    awaited_count=2,
    mutation=Doer(),
    crossover=TwoPoint(),
    selection=Roulette(),
    limit=WallTime('24:00:00'),
    method=Method(
        sampling=Const(count=32),
        function=GuessAndDetermine(
            # alpha_n=0,
            # time_limit=5,
            solver=Cadical5(),
            measure=SolvingTime(),
        ),
        executor=MPIExecutor(
            workers=4,
            shaping=Chunks(chunk_size=32)
        ),
    ),
    instance=Instance(
        cnf=CNF(path='multipliers/lec_CvK_16.cnf'),
        input_set=Variables([
            # *(Index(var) for var in SUPBS_VARS),
            *(Merged(f'x{i}', xor, group) for i, group in enumerate(XOR_GROUPS)),
            *(Merged(f'm{i}', majority, group) for i, group in enumerate(MAJ_GROUPS)),
            *(Merged(f'b{i}', bent_4, group) for i, group in enumerate(BENT4_GROUPS)),
            # xor permutations
            # *(Merged(f'x{j}|{i}', xor, group) for j, XOR_PERM_GROUPS in enumerate(XOR_PERM_LISTS)
            #   for i, group in enumerate(XOR_PERM_GROUPS)),
            # maj permutations
            *(Merged(f'm{j}|{i}', majority, group) for j, MAJ_PERM_GROUPS in enumerate(MAJ_PERM_LISTS)
              for i, group in enumerate(MAJ_PERM_GROUPS)),
            # bent permutations
            # *(Merged(f'b{j}|{i}', bent_4, group) for j, BENT4_PERM_GROUPS in enumerate(BENT4_PERM_LISTS)
            #   for i, group in enumerate(BENT4_PERM_GROUPS)),
        ]),
    ),
    output=JSONOut(path='other/lec_CvK_16'),
)
if __name__ == '__main__':
    backdoor = algorithm.instance.get_backdoor()
    print(len(backdoor))
    solution = algorithm.start_from_backdoors(backdoor)
