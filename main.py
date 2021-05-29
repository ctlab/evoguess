import sys
import json
from util import build

from output import Output
from method import Method
from executor import Executor
from function import Function
from instance import Instance
from algorithm import Algorithm

from instance._type.variables import BaseBackdoor

if __name__ == '__main__':
    assert len(sys.argv) == 2, f'Invalid number of input args {len(sys.argv)}'
    configuration = json.loads(sys.argv[1])

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

    backdoor = BaseBackdoor(2, algorithm.instance.secret_key)
    solution = algorithm.start(backdoor)
