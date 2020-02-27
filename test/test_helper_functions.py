import unittest
import numpy as np
from test.test_utility import TestUtility
from braphy.utility.helper_functions import *

class TestHelperFunctions(TestUtility):
    def test_divide_without_warning_1(self):
        a = np.array([[-1, -2, 3],
                      [-4, 5, 6],
                      [-7, 8, -9]])
        b = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        c = divide_without_warning(a, b)
        true_c = np.array([[-np.inf, -2, 0],
                           [np.nan, 0, -6],
                           [np.nan, 0, -np.inf]])
        self.assertMatrixEqual(c, true_c)

    def test_divide_without_warning_2(self):
        a = 1
        b = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        c = divide_without_warning(a, b)
        true_c = np.array([[np.inf, 1, 0],
                           [np.nan, 0, -1],
                           [np.nan, 0, np.inf]])
        self.assertMatrixEqual(c, true_c)

    def test_divide_without_warning_3(self):
        a = -1
        b = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        c = divide_without_warning(a, b)
        true_c = np.array([[-np.inf, -1, 0],
                           [np.nan, 0, 1],
                           [np.nan, 0, -np.inf]])
        self.assertMatrixEqual(c, true_c)

    def test_divide_without_warning_4(self):
        a = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        b = 0
        c = divide_without_warning(a, b)
        true_c = np.array([[np.nan, np.inf, np.inf],
                           [np.nan, -np.inf, -np.inf],
                           [np.nan, np.inf, np.nan]])
        self.assertMatrixEqual(c, true_c)

    def test_multiply_without_warning_1(self):
        a = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        b = 1
        c = multiply_without_warning(a, b)
        true_c = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        self.assertMatrixEqual(c, true_c)

    def test_multiply_without_warning_2(self):
        a = np.array([[-1, np.nan, 3],
                      [np.inf, -np.inf, 0],
                      [-7, 8, -np.inf]])
        b = np.array([[0, 1, np.inf],
                      [np.nan, -np.inf, -1],
                      [np.nan, np.inf, 0]])
        c = multiply_without_warning(a, b)
        true_c = np.array([[0, np.nan, np.inf],
                      [np.nan, np.inf, 0],
                      [np.nan, np.inf, np.nan]])
        self.assertMatrixEqual(c, true_c)


if __name__ == '__main__':
    unittest.main()