import os
import re
import threading

from util.collection import trim
from util.const import TEMPLATE_PATH

cnf_source = {}
cnf_clauses = {}
cnf_max_literal = {}
lock = threading.Lock()
numeral = re.compile('^[-0-9]')


class CNF:
    slug = 'cnf'
    name = 'CNF'
    has_atmosts = False

    def __init__(self, path):
        self._path = path
        self.path = os.path.join(TEMPLATE_PATH, path)

    def _parse(self):
        if self.path in cnf_clauses:
            return

        lines, clauses, max_lit = [], [], 0
        print(f'parse cnf... ({self.path})')
        with open(self.path) as handle:
            for line in handle.readlines():
                if line[0] in ['p', 'c']:
                    continue

                clause = [int(n) for n in line.split()]
                max_lit = max(max_lit, *map(abs, clause))
                clauses.append(trim(clause))
                lines.append(line)

        cnf_clauses[self.path] = clauses
        cnf_max_literal[self.path] = max_lit
        cnf_source[self.path] = ''.join(lines)

    def source(self, assumptions=()):
        with lock:
            self._parse()
            return ''.join([
                f'p cnf {cnf_max_literal[self.path]} ',
                f'{len(cnf_clauses[self.path]) + len(assumptions)}\n',
                cnf_source[self.path], *(f'{x} 0\n' for x in assumptions)
            ])

    def clauses(self):
        with lock:
            self._parse()
            return cnf_clauses[self.path]

    def max_literal(self):
        with lock:
            self._parse()
            return cnf_max_literal[self.path]

    def __copy__(self):
        return CNF(self._path)

    def __info__(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'path': self._path,
        }


__all__ = [
    'CNF'
]
