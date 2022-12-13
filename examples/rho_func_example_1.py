# algorithm module imports
from algorithm.impl import Elitism
from algorithm.module.mutation import Doer
from algorithm.module.crossover import TwoPoint
from algorithm.module.selection import Roulette

# function module imports
from function.impl import RhoFunction
from function.module.solver import pysat
from function.module.measure import Propagations

# instance module imports
from instance.impl import Instance
from instance.module.encoding import CNF
from typings.work_path import WorkPath

# space submodule imports
from core.module.space import SearchSet
from instance.module.variables import Interval

# executor module imports
from executor.impl import ProcessExecutor

# core submodule imports
from core.module.sampling import Const
from core.module.limitation import WallTime

# other imports
from core.impl import Optimize
from output.impl import VectorLogs
from core.module.comparator import MinValueMaxSize

if __name__ == '__main__':
    algorithm = Elitism(
        elites_count=2,
        population_size=6,
        mutation=Doer(),
        crossover=TwoPoint(),
        selection=Roulette(),
        min_update_size=6
    )
    function = RhoFunction(
        penalty_power=2 ** 10,
        measure=Propagations(),
        solver=pysat.Glucose3()
    )
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('sgen_150.cnf')
    instance = Instance(
        encoding=CNF(from_file=cnf_file)
    )  # read from file './examples/data/sgen_150.cnf
    space = SearchSet(
        by_mask=[],
        variables=Interval(start=1, length=150)
    )  # for search space of 150 “off” vars
    executor = ProcessExecutor(max_workers=16)
    sampling = Const(size=1024, split_into=256)
    limitation = WallTime(from_string='04:00:00')
    # log process to dir './examples/logs/<date_date>
    logs_path = root_path.to_path('logs')
    solution = Optimize(
        space=space,
        instance=instance,
        executor=executor,
        sampling=sampling,
        function=function,
        algorithm=algorithm,
        limitation=limitation,
        comparator=MinValueMaxSize(),
        logger=VectorLogs(logs_path),
    ).launch()

    for point in solution:
        print(point)
