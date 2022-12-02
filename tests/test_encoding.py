import unittest
from copy import copy

from typings.work_path import WorkPath
from instance.module.encoding import CNF, CNFP, CNFData, CNFPData


class TestEncodings(unittest.TestCase):
    def test_cnf_from_clause(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        assumptions, constraints = [1, 2, 3], [[-5, 2, -3]]

        cnf = CNF(from_clauses=clauses)
        cnf_data = cnf.get_data()
        # cnf.__info__()

        self.assertIsInstance(cnf_data, CNFData)
        self.assertEqual(cnf_data.max_literal, 4)
        self.assertEqual(cnf_data.clauses(), clauses)
        self.assertEqual(cnf_data.clauses(constraints), [*clauses, *constraints])

        self.assertEqual(
            cnf_data.source(),
            'p cnf 4 4\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n'
        )
        self.assertEqual(
            cnf_data.source((assumptions, [])),
            'p cnf 4 7\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n1 0\n2 0\n3 0\n'
        )
        self.assertEqual(
            cnf_data.source(([], constraints)),
            'p cnf 4 5\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n-5 2 -3 0\n'
        )
        self.assertEqual(
            cnf_data.source((assumptions, constraints)),
            'p cnf 4 8\n1 2 0\n2 3 0\n-1 2 3 0\n-4 1 2 0\n1 0\n2 0\n3 0\n-5 2 -3 0\n'
        )

    def test_cnf_from_file(self):
        root_path = WorkPath('examples', 'data', root='..')
        cnf = CNF(from_file=root_path.to_file('a5_1.cnf'))
        cnf_data = cnf.get_data()
        # cnf.__info__()

        self.assertEqual(cnf_data.clauses()[0], [65, 9, 30])
        self.assertEqual(cnf_data.clauses()[16], [-68, 17, 65])
        self.assertEqual(cnf_data.clauses()[1228], [-335, 268, 333])
        self.assertEqual(cnf_data.clauses()[-1], [-8425, -8293, -8295, 8297])
        self.assertEqual(cnf_data.source(), cnf.get_raw_data())

        cnf_copy = copy(cnf)
        cnf_copy_data = cnf_copy.get_data()

        self.assertEqual(cnf_data.source(), cnf_copy_data.source())
        self.assertEqual(cnf_data.clauses(), cnf_copy_data.clauses())
        self.assertEqual(cnf_data.max_literal, cnf_copy_data.max_literal)

    def test_cnfp_from_clause(self):
        clauses = [[1, 2], [2, 3], [-1, 2, 3], [-4, 1, 2]]
        assumptions, constraints = [1, 2, 3], [[-5, 2, -3]]

        cnf = CNFP(from_clauses=clauses, from_atmosts=[])
        cnfp_data = cnf.get_data()

        cnf_data = cnf.get_data()
        # cnf.__info__()

        # todo: extend cnfp tests
        self.assertIsInstance(cnf_data, CNFPData)
        self.assertEqual(cnf_data.max_literal, 4)
        self.assertEqual(cnf_data.clauses(), clauses)
