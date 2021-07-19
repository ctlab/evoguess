import sys
import json
from util import build

from output import Output
from method import Method
from executor import Executor
from function import Function
from instance import Instance
from algorithm import Algorithm

from instance.typings.variables import BaseBackdoor

if __name__ == '__main__':
    assert len(sys.argv) == 2, f'Invalid number of input args {len(sys.argv)}'
    configuration = json.loads(sys.argv[1])

    _, algorithm = build({
        Algorithm: [
            Output,
            Instance,
            {
                Method: [
                    Function,
                    Executor
                ]},
        ]}, **configuration
    )

    backdoor_line = configuration['backdoors'][0]
    backdoor = algorithm.instance.get_backdoor(**backdoor_line)
    solution = algorithm.start(backdoor)
