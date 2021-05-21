import re
import threading

from util.array import trim

cnf_clauses = {}
lock = threading.Lock()
numeral = re.compile('^[-0-9]')


class CNF:
    slug = 'cnf'
    name = 'CNF'

    def __init__(self, path):
        self.path = path

    def clauses(self):
        with lock:
            if self.path in cnf_clauses:
                return cnf_clauses[self.path]

            clauses = []
            print('parse cnf... (%s)' % self.path)
            with open(self.path) as f:
                for line in f.readlines():
                    if line[0] in ['p', 'c']:
                        continue

                    clause = [int(n) for n in line.split()]
                    clauses.append(trim(clause))

            cnf_clauses[self.path] = clauses
            return clauses

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
