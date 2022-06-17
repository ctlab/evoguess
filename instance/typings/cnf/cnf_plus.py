import os
import re
import threading

from util.const import TEMPLATE_PATH
from pysat.formula import CNFPlus as CNFP

cnf_instance = {}
lock = threading.Lock()
numeral = re.compile('^[-0-9]')


class CNFPlus:
    slug = 'cnf_plus'
    name = 'CNF+'
    has_atmosts = True

    def __init__(self, path):
        self._path = path
        self.path = os.path.join(TEMPLATE_PATH, path)

    def _parse(self):
        if self.path in cnf_instance:
            return

        cnfp = CNFP(from_file=self.path)
        cnf_instance[self.path] = cnfp

    def clauses(self, constraints=()):
        with lock:
            self._parse()
            return [
                *cnf_instance[self.path].clauses,
                *constraints
            ]

    def atmosts(self):
        with lock:
            self._parse()
            return cnf_instance[self.path].atmosts

    def max_literal(self):
        with lock:
            self._parse()
            return cnf_instance[self.path].nv

    def __copy__(self):
        return CNFPlus(self._path)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'path': self._path,
        }


__all__ = [
    'CNFPlus'
]
