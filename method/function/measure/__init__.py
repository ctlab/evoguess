from .impls.conflicts import *
from .impls.propagations import *
from .impls.solving_time import *
from .impls.learned_literals import *


def get(name):
    return {
        'confs': Conflicts,
        'time': SolvingTime,
        'props': Propagations,
        'lits': LearnedLiterals
    }[name]()


__all__ = [
    'get',
    'Conflicts',
    'SolvingTime',
    'Propagations',
    'LearnedLiterals'
]
