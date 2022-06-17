from algorithm.portfolio import Portfolio
from algorithm.portfolio.schema import Elitism, MuPlusLambda

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

from instance.cnf import CNF
from instance.impl import Instance
from instance.typings import Interval

from output.impl import JSONOut

if __name__ == '__main__':
    algorithm = Portfolio(
        schemas=[
            MuPlusLambda(
                mu=1, lmbda=1,
                mutation=Doer(),
                selection=Roulette(),
            ),
            Elitism(
                size=8, elites=2,
                mutation=Doer(),
                selection=Roulette(),
                crossover=TwoPoint(),
            )
        ],
        limit=WallTime('00:05:00'),
        method=Method(
            function=UPGuessAndDetermine(
                max_n=30,
                solver=Glucose3(),
                measure=Propagations(),
            ),
            executor=ProcessExecutor(
                workers=4,
                shaping=Chunks(chunk_rate=4)
            ),
            sampling=Const(count=100)
        ),
        instance=Instance(
            input_set=Interval(start=1, length=3244),
            cnf=CNF(path='sorting/pancake_vs_selection/pancake_vs_selection_7_4.cnf'),
        ),
        output=JSONOut(path='test/pvs/4_7'),
    )

    backdoor = algorithm.instance.get_backdoor()
    solution = algorithm.start_from_backdoors(backdoor)
