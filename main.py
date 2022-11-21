from core.impl import Optimize
from core.module.space import InputSet
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

from output.impl import VectorFull
from executor.impl import ThreadExecutor

from instance.impl import StreamCipher
from instance.module.encoding import CNF
from instance.module.variables import Interval

from function.impl import GuessAndDetermine
from function.module.measure import SolvingTime
from function.module.solver.impl.pysat import Glucose3

from algorithm.impl import MuPlusLambda
from algorithm.module.mutation import Doer
from algorithm.module.selection import Roulette

from typings.work_path import WorkPath

if __name__ == '__main__':
    data_path = WorkPath('evoguess_data', root='..')
    exps_path = data_path.to_path('experiments', 'testing')
    temps_path = data_path.to_path('templates')

    solution = Optimize(
        space=InputSet(),
        logger=VectorFull(exps_path),
        executor=ThreadExecutor(workers=4),
        sampling=Const(count=64, split_into=16),
        instance=StreamCipher(
            encoding=CNF(from_file=temps_path.to_file('a5_1.cnf')),
            input_set=Interval(start=1, length=64),
            output_set=Interval(start=8298, length=128)
        ),
        function=GuessAndDetermine(
            solver=Glucose3(),
            measure=SolvingTime(budget=2)
        ),
        algorithm=MuPlusLambda(
            mu_size=1,
            lambda_size=1,
            mutation=Doer(),
            selection=Roulette()
        ),
        comparator=MinValueMaxSize(),
        limitation=WallTime(from_string='00:05:00')
    ).launch()
    print(solution)

    # root = estimator.space.get_initial(estimator.instance)
    # result = estimator.estimate(root).result()
    # print(result.backdoor)
    # print(result.estimation)
