import json
import argparse

from output import Output
from method import Method
from executor import Executor
from function import Function
from instance import Instance
from algorithm import Algorithm

if __name__ == '__main__':
    from util import build

    parser = argparse.ArgumentParser(description='EvoGuess v2')
    parser.add_argument('-f', '--file', metavar='<configuration file>', type=str)
    parser.add_argument('-l', '--line', metavar='<configuration line>', type=str)

    args, _ = parser.parse_known_args()

    assert args.file or args.line, 'Specify one of the arguments -f or -l'

    if args.file:
        with open(args.file, 'r') as handle:
            configuration = json.load(handle)
    else:
        configuration = json.loads(args.line)

    _, algorithm = build(
        {Algorithm: [
            Output,
            Instance,
            {Method: [
                Function,
                Executor
            ]},
        ]}, **configuration
    )

    backdoors = [
        algorithm.instance.get_backdoor(**backdoor)
        for backdoor in configuration['backdoors']
    ]
    solution = algorithm.start_from_backdoors(*backdoors)
