from algorithm.impl import MuPlusLambda
from algorithm.module.limit import WallTime
from algorithm.module.evolution.mutation import Doer
from algorithm.module.evolution.selection import Roulette

from method.impl import Method
from method.module.sampling import Const

from function.impl import InverseBackdoorSets
from function.module.measure.impl import SolvingTime
from function.module.solver.impl.native import Cadical5

from executor.impl import ProcessExecutor
from executor.module.shaping.impl import Chunks

from instance.typings.cnf import CNF
from instance.impl import StreamCipher
from instance.typings.operator import xor
from instance.typings.var import Index, Merged
from instance.typings import Interval, Variables

from output.impl import JSONOut

INDEX_VARS = [78, 124, 142, 144, 146, 166, 188, 190, 208, 211, 212, 230, 256, 258, 278, 296, 298, 300, 322, 324,
              342, 344, 345, 366, 388, 409, 430, 433, 454, 500]

XOR_INDEXES = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18], [19, 20], [21, 22],
               [23, 24], [25, 26], [27, 28], [29, 30], [31, 32], [33, 34], [35, 36], [37, 38], [39, 40], [41, 42],
               [43, 44], [45, 46], [47, 48], [49, 50], [51, 52], [53, 54], [55, 56], [57, 58], [59, 60], [61, 62],
               [63, 64]]

if __name__ == '__main__':
    algorithm = MuPlusLambda(
        mu=1, lmbda=2,
        awaited_count=1,
        mutation=Doer(),
        selection=Roulette(),
        limit=WallTime('00:30:00'),
        method=Method(
            sampling=Const(count=32),
            function=InverseBackdoorSets(
                min_xi=0,
                time_limit=5,
                solver=Cadical5(),
                measure=SolvingTime(),
            ),
            executor=ProcessExecutor(
                workers=4,
                shaping=Chunks(chunk_rate=1)
            ),
        ),
        instance=StreamCipher(
            cnf=CNF(path='a5_1.cnf'),
            supbs=Interval(start=1, length=64),
            input_set=Variables([
                *(Index(var) for var in INDEX_VARS),
                *(Merged(f'x{i}', xor, group) for i, group in enumerate(XOR_INDEXES)),
            ]),
            output_set=Interval(start=8298, length=128)
        ),
        output=JSONOut(path='test/a5_1'),
    )

    backdoor = algorithm.instance.get_backdoor()
    solution = algorithm.start_from_backdoors(backdoor)
