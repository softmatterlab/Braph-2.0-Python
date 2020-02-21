import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_triangles import MeasureTriangles
from braphy.graph import *
import numpy as np

class TestTriangles(unittest.TestCase):
    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0,1,0],[1,0,0,1],[0,1,0,1],[0,0,0,0]])
        graph_bd = GraphBD(A, measure_list[GraphBD], 'zero')
        MeasureTriangles.compute_measure(graph_bd)
        self.assertSequenceEqual(graph_bd.measure_dict[MeasureTriangles]['triangles'].tolist(),
                                 [1, 1, 1, 0])

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0,1,0,0],[1,0,0,1,0],[0,1,0,1,0],[0,0,0,0,1],[0,0,0,1,0]])
        graph_bu = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        MeasureTriangles.compute_measure(graph_bu)
        self.assertSequenceEqual(graph_bu.measure_dict[MeasureTriangles]['triangles'].tolist(),
                                 [1, 2, 2, 1, 0])

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0,0.1,0.8],[0.5,0,0,0.2],[0,0.1,0,0.4],[0,0,0,0]])
        graph_wd = GraphWD(A, measure_list[GraphWD], 'zero')
        MeasureTriangles.compute_measure(graph_wd)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_wd.measure_dict[MeasureTriangles]['triangles'].tolist()[i], [0.0855, 0.0855, 0.0855, 0][i], places=4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0.5,0.1,0.8],[0.5,0,0.1,0.2],[0.1,0.1,0,0.4],[0.8,0.2,0.4,0]])
        graph_wu = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        MeasureTriangles.compute_measure(graph_wu)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_wu.measure_dict[MeasureTriangles]['triangles'].tolist()[i], [0.9194, 0.8019, 0.6885, 0.9484][i], places=4)

if __name__ == '__main__':
    unittest.main()
