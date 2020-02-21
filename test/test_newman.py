import unittest
from braphy.graph_measures import MeasureParser
from braphy.graph import *
import numpy as np

class TestNewman(unittest.TestCase):
    def test(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')


if __name__ == '__main__':
    unittest.main()
