import argparse
from os.path import join

import output
import method
import instance
import algorithm
import concurrency

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EvoGuess v1')
    parser.add_argument('instance', type=str, help='instance of problem')
    parser.add_argument('-t', '--threads', metavar='4', type=int, default=4, help='count of threads')
    parser.add_argument('-o', '--output', metavar='str', type=str, default='main', help='output subdir')
    parser.add_argument('-b', '--backdoor', metavar='str', type=str, default='*', help='start backdoor')
    parser.add_argument('-n', '--sampling', metavar='str', type=str, default='1000', help='sampling function')
    parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
    parser.add_argument('-v', '--verbosity', metavar='3', type=int, default=3, help='debug [0-3] verbosity level')
    parser.add_argument('-a', '--algorithm', metavar='str', type=str, default='1+1', help='optimization algorithm')

    parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
    parser.add_argument('-m', '--measure', metavar='str', type=str, default='props', help='measure of estimation')

    args, _ = parser.parse_known_args()

    # seeds
    # concurrency_seed, method_seed = 3665729543, 4294967295
    # m_seed, c_seed, s_seed = 4294967295, 4294967295, 4294967295
    concurrency_seed, method_seed = None, None
    m_seed, c_seed, s_seed = None, None, None

    # instance
    _instance = instance.get_instance(args.instance)
    assert _instance.check(), "Cnf is missing: %s" % _instance.cnf_path

    # output
    path = ['output', '_%s_logs' % args.output, _instance.tag, _instance.type]
    _output = output.Output(
        dverb=args.verbosity,
        path=join(*[f for f in path if f is not None]),
    ).open().touch()

    _concurrency = concurrency.ProcessExecutor(
        workload=0,
        output=_output,
        threads=args.threads,
        random_seed=concurrency_seed,
    )

    _method = method.Method(
        output=_output,
        random_seed=method_seed,
        concurrency=_concurrency,
        sampling=method.sampling.get_sampling(args.sampling),
        function=method.function.GuessAndDetermine(
            instance=_instance,
            solver=method.solver.pysat.get(args.solver, use_keys=True),
            measure=method.function.measure.get(args.measure),
        )
    )

    Algorithm, alg_kwargs = algorithm.get_algorithm(args.algorithm)
    _algorithm = Algorithm(
        **alg_kwargs,
        output=_output,
        method=_method,
        limit=algorithm.limit.WallTime(args.walltime),
        mutation=algorithm.evolution.mutation.Doer(seed=m_seed),
        selection=algorithm.evolution.selection.Best(seed=s_seed),
        crossover=algorithm.evolution.crossover.Uniform(prob=0.2, seed=c_seed),
    )

    backdoor = _instance.get_backdoor(args.backdoor)
    points = _algorithm.start(backdoor)
    map(print, points)

    _output.close()
