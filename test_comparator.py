from unittest import TestCase
from comparator import *

class Test(TestCase):

    def test_big_ol_comparator_compares_properly(self):
        bit_string_len = 4
        max_number = 2 ** bit_string_len
        ret = []
        for i in range(max_number):
            A = format(i, 'b').zfill(bit_string_len)
            A_bool = []
            for binary in A:
                A_bool.append(bool(int(binary)))
            for j in range(max_number):
                B = format(j, 'b').zfill(bit_string_len)
                B_bool = []
                for binary in B:
                    B_bool.append(bool(int(binary)))
                    self.assertEqual(two_four_bit_comparator(A_bool[0], A_bool[1], A_bool[2], A_bool[3], B_bool[0], B_bool[1], B_bool[2], B_bool[3])[0], i >= j)

    def test_two_four_bit_comparator_is_reversible(self):
        bit_string_len = 4
        max_number = 2 ** bit_string_len
        ret = []
        for i in range(max_number):
            A = format(i, 'b').zfill(bit_string_len)
            A_bool = []
            for binary in A:
                A_bool.append(bool(int(binary)))
            for j in range(max_number):
                B = format(j, 'b').zfill(bit_string_len)
                B_bool = []
                for binary in B:
                    B_bool.append(bool(int(binary)))
                ret = two_four_bit_comparator(A_bool[0], A_bool[1], A_bool[2], A_bool[3], B_bool[0], B_bool[1], B_bool[2], B_bool[3])
                actual = two_four_bit_comparator(ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7])
                full_input = A + B
                for k in range(1, len(ret)):
                    full_input_bool = bool(int(full_input[k]))
                    actual_bool = actual[k]
                    self.assertEqual(full_input_bool, actual_bool)

        ret.sort()
        pprint.pprint(ret)