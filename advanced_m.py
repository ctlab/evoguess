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
from instance.typings import Variables
from instance.module.encoding import CNF

from output.impl import JSONOut

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
        encoding=CNF(from_file='multipliers/lec_CvK_16.cnf'),
        input_set=Variables.from_file('_variables/lec_maj_vars.json')
    ),
    output=JSONOut(path='other/lec_CvK_16'),
)
if __name__ == '__main__':
    backdoor = algorithm.instance.get_backdoor()
    print(len(backdoor))
    solution = algorithm.start_from_backdoors(backdoor)
