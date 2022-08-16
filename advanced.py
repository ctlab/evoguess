from algorithm.impl import Elitism
from algorithm.module.limit import WallTime
from algorithm.module.evolution.mutation import Doer
from algorithm.module.evolution.selection import Roulette
from algorithm.module.evolution.crossover import TwoPoint

from method.impl import Method
from method.module.sampling import Const

from function.impl import UPGuessAndDetermine
from function.module.measure.impl import Propagations
from function.module.solver.impl.pysat import Glucose3

from executor.impl import ProcessExecutor
from executor.module.shaping.impl import Chunks

from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Interval

from output.impl import JSONOut

if __name__ == '__main__':
    algorithm = Elitism(
        awaited_count=2,
        size=8, elites=2,
        mutation=Doer(),
        selection=Roulette(),
        crossover=TwoPoint(),
        limit=WallTime('12:00:00'),
        method=Method(
            function=UPGuessAndDetermine(
                max_n=30,
                solver=Glucose3(),
                measure=Propagations(),
            ),
            executor=ProcessExecutor(
                workers=4,
                shaping=Chunks(chunk_size=16)
            ),
            sampling=Const(count=64)
        ),
        instance=Instance(
            encoding=CNF(from_file='sort/pvs_4_7.cnf'),
            search_set=Interval(start=1, length=28),
        ),
        output=JSONOut(path='test/pvs/4_7'),
    )

    backdoor = algorithm.instance.get_backdoor(by_mask=[])
    solution = algorithm.start_from_backdoors(backdoor)
