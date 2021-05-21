from . import limit
from .evolution import *

modules = {
    **limit.limits,
    **mutation.mutations,
    **crossover.crossovers,
    **selection.selections,
}
