import json
import argparse

from method.typings.handle import n_completed

from output import Output
from method import Method
from executor import Executor
from function import Function
from instance import Instance

if __name__ == '__main__':
    from util import build

    parser = argparse.ArgumentParser(description='EvoGuess v2 verify')
    parser.add_argument('-f', '--file', metavar='<configuration file>', type=str)
    parser.add_argument('-l', '--line', metavar='<configuration line>', type=str)
    args, _ = parser.parse_known_args()

    assert args.file or args.line, 'Specify one of the arguments -f or -l'

    if args.file:
        with open(args.file, 'r') as handle:
            configuration = json.load(handle)
    else:
        configuration = json.loads(args.line)

    _, method = build(
        {Method: [
            Function,
            Executor
        ]}, **configuration
    )
    output = Output(configuration['output'])
    instance = Instance(configuration['instance'])
    backdoors = [
        instance.get_backdoor(**backdoor)
        for backdoor in configuration['backdoors']
    ]

    bd_handles = []
    output.open('method')
    output.info(
        output=output.__info__(),
        method=method.__info__(),
        instance=instance.__info__(),
        backdoors=configuration['backdoors']
    )
    for backdoor in backdoors:
        handle = method.queue(instance, backdoor)
        bd_handles.append((backdoor, handle))

    while len(bd_handles) > 0:
        handles = [h for (_, h) in bd_handles]
        done = n_completed(handles, 1)

        estimated, left_bd_handles = [], []
        for bd, handle in bd_handles:
            if handle not in done:
                left_bd_handles.append((bd, handle))
            else:
                estimation = handle.result()
                output.log({'backdoor': repr(bd), 'size': len(bd), **estimation})

        bd_handles = left_bd_handles

    method.executor.shutdown()
    output.close()
