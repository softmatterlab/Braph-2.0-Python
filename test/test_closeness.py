import unittest
from braphy.graph_measures import *
from braphy.graph import *
import numpy as np
from test.test_utility import TestUtility

class TestCloseness(TestUtility):
    
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 0, 1, 1, 1],
                      [0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        closeness = [1/1.458333, 1/1.5833, 1/1.1250, np.nan, 1/1.2500]
        closeness_in = [1/1.6667, 1/1.6667, 1/1.0, 1/1.5, 1/1.0]
        closeness_out = [1/1.25, 1/1.5, 1/1.25, np.nan, 1/1.5]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_in').tolist(),
                                       closeness_in, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_out').tolist(),
                                       closeness_out, 4)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 0, 1, 1, 1],
                      [0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        closeness = [1/1.25, 1/1.5, 1/1.0, 1/1.5, 1/1.25]
        self.assertSequenceEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                 closeness)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        closeness = [1/0.2329305, 1/0.1532128, 1/0.1690614, 1/0.1803302, 1/0.1532128]
        closeness_in = [1/0.1079295, 1/0.2437677, 1/0.1230042, 1/0.21635105, 1/0.1977864]
        closeness_out = [1/0.3579316, 1/0.0627490, 1/0.2151187, 1/0.1443093, 1/0.1086391]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, 2)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_in').tolist(),
                                       closeness_in, 2)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_out').tolist(),
                                       closeness_out, 2)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        closeness = [1/0.1079, 1/0.0612, 1/0.0535, 1/0.1341, 1/0.0527]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, places = 1)

    def test_wu_2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWU(A, measure_list[GraphWU])
        closeness = [0.0966, 0.1284, 0.1647, 0.1284, 0.1647, 0.0859, 0.1505, 0.1359]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, places = 4)

 
if __name__ == '__main__':
    unittest.main()