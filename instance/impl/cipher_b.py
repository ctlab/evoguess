from .cipher_s import *

from util.array import concat
from ..module.variables import Variables
from ..module.variables.vars import Supplements, compress

from numpy.random import RandomState


class BlockCipher(StreamCipher):
    slug = 'cipher:block'

    def __init__(self, plain_set: Variables, **kwargs):
        self.plain_set = plain_set
        super().__init__(**kwargs)

    def _get_inversion_deps(self, *args: Variables):
        return [
            *self.plain_set.variables(),
            *super()._get_inversion_vars(*args)
        ]

    def _get_propagation_sups(self, state: RandomState) -> Supplements:
        var_deps = self.plain_set.get_var_deps()
        deps_bases = self.plain_set.get_deps_bases()
        deps_values = {
            var: value for var, value in
            zip(var_deps, state.randint(0, deps_bases))
        }
        return compress(
            super()._get_propagation_sups(state),
            *(var.supplements(deps_values) for var in self.input_set)
        )

    def __info__(self):
        return {
            **super().__info__(),
            'plain_set': self.plain_set.__info__(),
        }
