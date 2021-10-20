import os
import re
import threading

from util.array import trim
from util.const import TEMPLATE_PATH

cnf_clauses = {}
cnf_variables = {}
cnf_max_literal = {}
lock = threading.Lock()
numeral = re.compile('^[-0-9]')


class CNF:
    slug = 'cnf'
    name = 'CNF'

    def __init__(self, path):
        self.path = os.path.join(TEMPLATE_PATH, path)

    def _parse(self):
        if self.path in cnf_clauses:
            return

        clauses, variables = [], set()
        print('parse cnf... (%s)' % self.path)
        with open(self.path) as f:
            for line in f.readlines():
                if line[0] in ['p', 'c']:
                    continue

                clause = trim([int(n) for n in line.split()])
                variables.update(map(abs, clause))
                clauses.append(clause)

        cnf_clauses[self.path] = clauses
        cnf_variables[self.path] = variables
        cnf_max_literal[self.path] = max(variables)

    def clauses(self):
        with lock:
            self._parse()
            return cnf_clauses[self.path]

    def variables(self):
        with lock:
            self._parse()
            return cnf_variables[self.path]

    def max_literal(self):
        with lock:
            self._parse()
            return cnf_max_literal[self.path]

    def __copy__(self):
        return CNF(self.path)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'path': self.path,
        }


__all__ = [
    'CNF'
]
