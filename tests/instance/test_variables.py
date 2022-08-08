import unittest

from instance.typings import Interval, Backdoor
from instance.typings.var import Index, Domain, Switch, compress


class TestVariables(unittest.TestCase):
    def test_interval(self):
        interval = Interval(1, 64)
        self.assertEqual(len(interval), 64)
        self.assertEqual(str(interval), '1..64')
        self.assertEqual(repr(interval), '[1..64](64)')

        for i, variable in enumerate(interval):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 1))

        interval = Interval._from(str(interval))
        self.assertEqual(str(interval), '1..64')

    def test_backdoor_index(self):
        str_backdoor = '1 5 9 12 17 21 23 24 25 35'
        backdoor = Backdoor._from(str_backdoor)
        self.assertEqual(len(backdoor), 10)
        self.assertEqual(str(backdoor), str_backdoor)
        self.assertEqual(repr(backdoor), f'[{str_backdoor}](10)')

        str_vars = str_backdoor.split(' ')
        for i, variable in enumerate(backdoor):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str_vars[i])

        int_vars = list(set(map(int, str_vars)))
        self.assertEqual(backdoor.get_var_deps(), int_vars)
        self.assertEqual(backdoor.get_deps_bases(), [2] * len(int_vars))

        backdoor = Backdoor([
            Domain('d1', [1, 2, 3, 4, 5, 6]),
            Index(7), Index(8), Index(9), Index(10),
            Switch('x1', lambda *args: sum(args) % 2 == 1, [11, 12]),
            Switch('x2', lambda *args: sum(args) % 2 == 1, [13, 14])
        ])

        values = [4, 1, 1, 0, 0, 1, 0]
        alters = ['d1', 7, 8, 9, 10, 'x1', 'x2']
        variables = backdoor.variables()
        for var, alt in zip(variables, alters):
            self.assertEqual(var, alt)
        self.assertEqual(str(backdoor), 'd1 7 8 9 10 x1 x2')

        value_dict = {var: value for var, value in zip(backdoor, values)}
        self.assertEqual(value_dict[7], 1)
        self.assertEqual(value_dict['d1'], 4)
        assumptions, constraints = compress(*(
            var.supplements(value_dict) for var in backdoor
        ))
        self.assertEqual(assumptions, [-1, -2, -3, -4, 5, -6, 7, 8, -9, -10])
        self.assertEqual(constraints, [[11, 12], [-11, -12], [13, -14], [-13, 14]])


if __name__ == '__main__':
    unittest.main()
