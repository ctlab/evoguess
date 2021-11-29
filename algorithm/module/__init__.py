from .evolution import *

modules = {
    **mutation.mutations,
    **crossover.crossovers,
    **selection.selections,
}
