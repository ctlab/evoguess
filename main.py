from core.impl import Optimize
from core.module.space import InputSet
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from output.impl import VectorLogs
from executor.impl import ThreadExecutor

from instance.impl import StreamCipher
from instance.module.encoding import CNF
from instance.module.variables import Interval

from function.impl import InverseBackdoorSets
from function.module.measure import SolvingTime
from function.module.solver.impl.pysat import Glucose3

from algorithm.impl import Elitism
from algorithm.module.mutation import Doer
from algorithm.module.crossover import TwoPoint
from algorithm.module.selection import Roulette

from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    logs_path = root_path.to_path('logs')
    data_path = root_path.to_path('data')

    solution = Optimize(
        space=InputSet(),
        logger=VectorLogs(logs_path),
        executor=ThreadExecutor(max_workers=2),
        sampling=Const(value=64, split_into=16),
        instance=StreamCipher(
            encoding=CNF(from_file=data_path.to_file('a5_1.cnf')),
            input_set=Interval(start=1, length=64),
            output_set=Interval(start=8298, length=128)
        ),
        function=InverseBackdoorSets(
            solver=Glucose3(),
            measure=SolvingTime(budget=1.)
        ),
        algorithm=Elitism(
            elites_count=2,
            population_size=4,
            mutation=Doer(),
            crossover=TwoPoint(),
            selection=Roulette()
        ),
        comparator=MinValueMaxSize(),
        limitation=WallTime(from_string='00:01:00')
    ).launch()

    for point in solution:
        print(point)
