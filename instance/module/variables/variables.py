from .vars import Var, VarDeps
from .var_tools import parse_vars_raw

from typing import List
from os.path import join
from threading import Lock
from itertools import chain

from util.const import TEMPLATE_PATH
from util.lazy_file import get_file_data

vars_data = {}
parse_lock = Lock()


class Variables:
    slug = 'variables'

    def __init__(self, from_vars: List[Var] = None, from_file: str = None):
        self.filepath = from_file
        self._variables = from_vars

        self._var_deps = None
        self._var_bases = None
        self._deps_bases = None

    def _process_vars_raw(self):
        with parse_lock:
            if self.filepath in vars_data:
                return

            vars_raw = get_file_data(join(TEMPLATE_PATH, self.filepath))
            vars_data[self.filepath] = parse_vars_raw(vars_raw)

    def variables(self) -> List[Var]:
        if self._variables:
            return self._variables
        elif self.filepath in vars_data:
            return vars_data[self.filepath]

        self._process_vars_raw()
        return vars_data[self.filepath]

    def _upd_var_deps(self):
        self._var_deps = list(set(chain(*[
            v.deps for v in self.variables()
        ])))

    def get_var_deps(self) -> List[VarDeps]:
        if not self._var_deps:
            self._upd_var_deps()
        return self._var_deps

    def _upd_var_bases(self):
        self._var_bases = [
            v.base for v in self.variables()
        ]

    def get_var_bases(self) -> List[int]:
        if not self._var_bases:
            self._upd_var_bases()
        return self._var_bases

    def _upd_deps_bases(self):
        self._deps_bases = [
            2 if isinstance(v, int) else
            v.base for v in self.get_var_deps()
        ]

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

    def __info__(self):
        return {
            'slug': self.slug,
            'from_file': self.filepath,
        }


__all__ = [
    'Var',
    'List',
    'VarDeps',
    'Variables',
]
