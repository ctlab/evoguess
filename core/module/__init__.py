from . import limitation, sampling, comparator

modules = {
    **sampling.impls,
    **comparator.impls,
    **limitation.impls,
}
