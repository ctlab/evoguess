import os
import json

from .operator import *
from itertools import chain
from typing import Dict, List
from util.const import TEMPLATE_PATH
from .var import Var, AnyVar, Index, Switch, Domain

# todo: remove in island based fw
variables_dict = {}
operations = {
    'xor': xor,
    'bent_4': bent_4,
    'majority': majority
}


def parse_var_file(path):
    if path not in variables_dict:
        variables = []
        temp_path = os.path.join(TEMPLATE_PATH, path)
        print(f'parse variables... ({temp_path})')
        with open(temp_path) as handle:
            var_scheme = json.load(handle)
        for key, value in var_scheme.items():
            if key.startswith('index'):
                variables.extend([Index(var) for var in value])
            elif key.startswith('switch'):
                prefix = value['prefix']
                op = operations[value['op']]
                variables.extend([
                    Switch(f'{prefix}{i}', op, group)
                    for i, group in enumerate(value['groups'])
                ])
            elif key.startswith('domain'):
                prefix = value['prefix']
                variables.extend([
                    Domain(f'{prefix}{i}', group)
                    for i, group in enumerate(value['groups'])
                ])
                variables.extend([])
            else:
                raise Exception('Unknown variable group key')

        variables_dict[path] = variables
    #
    return variables_dict[path]


VarRules = Dict[str, Var]


class Variables:
    slug = 'variables'
    name = 'Variables'

    # noinspection PyMissingConstructor
    def __init__(self, variables: List[Var]):
        self._path = None
        self._variables = variables

        self._var_deps = None
        self._var_bases = None
        self._deps_bases = None

    def variables(self) -> List[Var]:
        # todo: remove in island based fw
        if not self._variables:
            return parse_var_file(self._path)
        else:
            #
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
    def _from(string: str, rules: VarRules = ()) -> 'Variables':
        variables = []
        for lit in string.split(' '):
            try:
                variables.append(Index(int(lit)))
            except ValueError:
                variables.append(rules[lit])

        return Variables(variables)

    @staticmethod
    def from_file(path: str) -> 'Variables':
        variables = Variables(None)
        variables._path = path
        return variables

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'path': self._path,
        }


__all__ = [
    'Var',
    'List',
    'VarRules',
    'Variables',
    'parse_var_file'
]
