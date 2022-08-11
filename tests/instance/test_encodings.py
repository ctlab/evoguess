import unittest

from instance.module.encoding import CNF
from instance.module.encoding.impl import CNFData


class TestEncodings(unittest.TestCase):
    def test_cnf_from_clause(self):
        clauses = [
            [1, 2],
            [2, 3],
            [-1, 2, 3],
            [-4, 1, 2],
        ]
        constraints = [[-5, 2, -3]]
        assumptions = [1, 2, 3]

        cnf = CNF(from_clauses=clauses)
        cnf_data = cnf.get_data()
        cnf.__info__()

        self.assertEqual(type(cnf_data), CNFData)

        self.assertEqual(cnf_data.clauses(), clauses)
        self.assertEqual(cnf_data.clauses(constraints), [*clauses, *constraints])

        self.assertEqual(cnf_data.source(), 'p cnf 4 4\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n')
        self.assertEqual(cnf_data.source(assumptions), 'p cnf 4 7\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n1 0\n2 0\n3 0\n')
        self.assertEqual(cnf_data.source([], constraints), 'p cnf 4 5\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n-5 2 -3 0\n')
        self.assertEqual(
            cnf_data.source(assumptions, constraints),
            'p cnf 4 8\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n1 0\n2 0\n3 0\n-5 2 -3 0\n'
        )

    def test_cnf_from_file(self):
        cnf = CNF(from_file='a5_1.cnf')
        cnf_data = cnf.get_data()
        cnf.__info__()

        self.assertEqual(cnf_data.clauses()[0], [65, 9, 30])
        self.assertEqual(cnf_data.clauses()[16], [-68, 17, 65])
        self.assertEqual(cnf_data.clauses()[1228], [-335, 268, 333])
        self.assertEqual(cnf_data.clauses()[-1], [-8425, -8293, -8295, 8297])
        self.assertEqual(cnf_data.source(), cnf.get_raw_data())
