from .evolution import *
from . import limit, tuner

modules = {
    **limit.limits,
    **tuner.tuners,
    **mutation.mutations,
    **crossover.crossovers,
    **selection.selections,
}
