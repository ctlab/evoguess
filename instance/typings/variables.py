from .var import Index, Var, AnyVar

from itertools import chain
from typing import Dict, List

VarRules = Dict[str, Var]


class Variables:
    slug = 'variables'
    name = 'Variables'

    # noinspection PyMissingConstructor
    def __init__(self, variables: List[Var] = ()):
        self._variables = variables

        self._var_deps = None
        self._var_bases = None
        self._deps_bases = None

    def variables(self) -> List[Var]:
        return self._variables

    def get_var_deps(self) -> List[AnyVar]:
        if not self._var_deps:
            self._upd_var_deps()
        return self._var_deps

    def get_var_bases(self) -> List[int]:
        if not self._var_bases:
            self._upd_var_bases()
        return self._var_bases

    def get_deps_bases(self) -> List[int]:
        if not self._deps_bases:
            self._upd_deps_bases()
        return self._deps_bases

    def __len__(self):
        return len(self.variables())

    def __contains__(self, item):
        return item in self.variables()

    def __iter__(self):
        return self.variables().__iter__()

    def __hash__(self):
        return hash(tuple(self.variables()))

    def __repr__(self):
        return f"[{str(self)}]({len(self)})"

    def __str__(self):
        return ' '.join(map(str, self.variables()))

    def _upd_var_deps(self):
        self._var_deps = list(set(chain(*[
            v.deps for v in self.variables()
        ])))

    def _upd_var_bases(self):
        self._var_bases = [
            v.base for v in self.variables()
        ]

    def _upd_deps_bases(self):
        self._deps_bases = [
            2 if isinstance(v, int) else
            v.base for v in self.get_var_deps()
        ]

    @staticmethod
    def _from(string: str, rules: VarRules = ()):
        variables = []
        for lit in string.split(' '):
            try:
                variables.append(Index(int(lit)))
            except ValueError:
                variables.append(rules[lit])

        return Variables(variables)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
        }


__all__ = [
    'Var',
    'List',
    'VarRules',
    'Variables'
]
