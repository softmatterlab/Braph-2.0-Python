import unittest
from braphy.utility import *
from test.test_utility import TestUtility
import numpy as np

class TestStatFunctions(TestUtility):
    def test_fdr_1(self):
        p_values = np.array([0.0068, 0.0087, 0.0091, 0.0106, 0.0131,
                             0.0138, 0.0155, 0.0473, 0.0551, 0.0596])
        q = 0.05
        self.assertEqual(StatFunctions.false_discovery_rate(p_values, q), 0.0138)

    def test_fdr_2(self):
        p_values = np.array([0.0510, 0.0066, 0.0001, 0.0101, 0.0526,
                             0.0673, 0.0040, 0.0621, 0.0318, 0.0059])
        q = 0.6
        self.assertEqual(StatFunctions.false_discovery_rate(p_values, q), 0.0673)

    def test_quantiles(self):
        values = np.array([[-1.0546, -1.1122, 0.14],
                           [-0.3560, -0.8799, 0.0976],
                           [-1.2410, 1.3363, 1.7498]])
        P = 5
        answer = np.array([[-1.2410, -1.1122, 0.0976],
                           [-1.2322, -1.0877, 0.1141],
                           [-1.0552, -0.8918, 0.1472],
                           [-1.0552, -0.8918, 0.1472],
                           [-0.3648, 1.3118, 1.7333],
                           [-0.3560, 1.3363, 1.7498]])
        q = StatFunctions.quantiles(values, P)
        self.assertMatrixAlmostEqual(q, answer, 4)

    def test_p_value_one_tail(self):
        res = np.array([-0.8844, -0.0515, 1.4034])
        values = np.array([[2.1740, 0.5551, 0.4214],
                           [0.4005, -0.1353, 0.7243],
                           [0.3862, -0.6801, -0.9634],
                           [0.4223, 0.9550, 0.2082],
                           [1.6609, 0.1446, 0.0056],
                           [-1.1635, -0.3201, -0.0012],
                           [-2.1287, 0.5323, 3.6216],
                           [0.2990, 0.7428, -1.6284],
                           [-0.4872, 2.4419, -0.4194],
                           [0.4031, 1.7427, 0.8831]])
        self.assertSequenceEqual(StatFunctions.p_value_one_tail(res, values).tolist(),
                                 [0.2, 0.3, 0.1])

    def test_p_value_two_tail(self):
        res = np.array([-0.8844, -0.0515, 1.4034])
        values = np.array([[2.1740, 0.5551, 0.4214],
                           [0.4005, -0.1353, 0.7243],
                           [0.3862, -0.6801, -0.9634],
                           [0.4223, 0.9550, 0.2082],
                           [1.6609, 0.1446, 0.0056],
                           [-1.1635, -0.3201, -0.0012],
                           [-2.1287, 0.5323, 3.6216],
                           [0.2990, 0.7428, -1.6284],
                           [-0.4872, 2.4419, -0.4194],
                           [0.4031, 1.7427, 0.8831]])
        self.assertSequenceEqual(StatFunctions.p_value_two_tail(res, values).tolist(),
                                 [0.4, 0.5, 0.3])

if __name__ == '__main__':
    unittest.main()
