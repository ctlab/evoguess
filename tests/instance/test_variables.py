import unittest

from instance.module.variables import Interval, Indexes, Backdoor
from instance.module.variables.vars import Index, Domain, Switch, compress


class TestVariables(unittest.TestCase):
    def test_interval(self):
        interval = Interval(start=1, length=64)
        self.assertEqual(len(interval), 64)
        self.assertEqual(str(interval), '1..64')
        self.assertEqual(repr(interval), '[1..64](64)')

        interval.__info__()
        for i, variable in enumerate(interval):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 1))

        interval = Interval(from_string=str(interval))
        self.assertEqual(str(interval), '1..64')

    def test_indexes(self):
        iterable = range(31, 67)
        indexes = Indexes(from_iterable=iterable)
        self.assertEqual(len(indexes), len(iterable))
        str_iterable = ' '.join(map(str, iterable))
        self.assertEqual(str(indexes), str_iterable)
        self.assertEqual(repr(indexes), f'[{str_iterable}]({len(iterable)})')

        indexes.__info__()
        for i, variable in enumerate(indexes):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str(i + 31))

        interval = Indexes(from_string=str(indexes))
        self.assertEqual(str(interval), str_iterable)

    def test_index_backdoor(self):
        str_iterable = '1 5 9 12 17 21 23 24 25 35'
        indexes = Indexes(from_string=str_iterable)
        backdoor = Backdoor(from_vars=indexes.variables())
        self.assertEqual(len(backdoor), 10)
        self.assertEqual(str(backdoor), str_iterable)
        self.assertEqual(repr(backdoor), f'[{str_iterable}](10)')

        self.assertEqual(backdoor._length, 10)
        self.assertEqual(backdoor._mask, [1] * 10)

        backdoor.__info__()
        str_vars = str_iterable.split(' ')
        for i, variable in enumerate(backdoor):
            self.assertIsInstance(variable, Index)
            self.assertEqual(variable.name, str_vars[i])

        int_vars = list(set(map(int, str_vars)))
        self.assertEqual(backdoor.get_var_deps(), int_vars)
        self.assertEqual(backdoor.get_deps_bases(), [2] * len(int_vars))

    def test_vars_backdoor(self):
        backdoor = Backdoor(from_vars=[
            Domain('d1', [1, 2, 3, 4, 5, 6]),
            Index(7), Index(8), Index(9), Index(10),
            Switch('x1', lambda *args: sum(args) % 2 == 1, [11, 12]),
            Switch('x2', lambda *args: sum(args) % 2 == 1, [13, 14])
        ])

        backdoor.__info__()
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
