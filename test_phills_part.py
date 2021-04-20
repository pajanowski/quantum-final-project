import math
from unittest import TestCase
import phills_part

class Test(TestCase):
    def test_get_superposition_n(self):
        v_0 = [
            [1],
            [0]
        ]

        v_1 = [
            [0],
            [1]
        ]

        v_2 = [
            [1],
            [1]
        ]

        v_5 = [
            [0],
            [1],
            [1]
        ]

        self.assertEqual(v_0, phills_part.get_superposition(0, 1))
        self.assertEqual(v_1, phills_part.get_superposition(1, 1))
        self.assertEqual(v_2, phills_part.get_superposition(2, 2))
        self.assertEqual(v_5, phills_part.get_superposition(5, math.ceil(math.log(5, 2))))

