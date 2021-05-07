import math
import random
from unittest import TestCase
import phills_part


class Test(TestCase):
    def test_truth_table_generator(self):
        phills_part.N = 16
        phills_part.L = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        phills_part.y = 4
        table = phills_part.get_truth_table()
        expected = '1111000000000000'
        self.assertEqual(expected, table)

        phills_part.N = 4
        phills_part.L = [1, 0, 3, 2]
        phills_part.y = 2
        expected = '1101'
        table = phills_part.get_truth_table()
        self.assertEqual(expected, table)

    def test_boolean_function_getter(self):
        phills_part.N = 4
        phills_part.L = [1, 0, 3, 2]
        phills_part.y = 2

        function = phills_part.get_boolean_functions_from_truth_table().strip()
        # truth table will be 1101
        # so for index 0 we will get back 00 so its specific function will be ( not {0} and not {1} )
        # but we only want it returning true on the 1 states
        expected = '''
            ( not {0} and not {1} ) or ( not {0} and {1} ) or ( {0} and {1} )
        '''.replace('\n', '').strip()
        self.assertEqual(expected, function)