from . import worker_t
from .worker_t import *

from ..module.solver.solver import Solver
from ..module.measure.measure import Measure

from typing import Any, Callable, Dict, Tuple

from core.module.space import Space
from instance.impl.instance import Instance
from instance.module.variables.impl.backdoor import ByteMask

Payload = Tuple[
    Space,
    Solver,
    Measure,
    Instance,
    ByteMask
]

WorkerCallable = Callable[
    [WorkerArgs, Payload],
    WorkerResult
]

Estimation = Dict[str, Any]

__all__ = [
    'Payload',
    'Estimation',
    'WorkerCallable',
    *worker_t.__all__
]
