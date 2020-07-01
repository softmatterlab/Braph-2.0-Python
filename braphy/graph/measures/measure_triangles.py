from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy
from numpy.linalg import matrix_power, multi_dot

class MeasureTriangles(Measure):
    def dimensions():
        d = {}
        d['triangles'] = Measure.NODAL
        return d

    def get_description():
        description = {}
        description['triangles'] = 'The number of triangles around a node is the numbers of couples of ' +\
                                    'node neighbors that are connected.'
        return description

    def compute_measure(graph):
        measure_dict = {}
        A = graph.A.copy()

        if graph.is_undirected():
            triangles = np.diag(matrix_power(np.power(A,1/3),3)) / 2
            triangles[np.isnan(triangles)] = 0

        else:
            directed_triangles_rule = 'cycle' # change default or set input from user here if wanted
            if directed_triangles_rule == 'all':
                triangles = np.diag(matrix_power(np.power(A,1/3) + np.power(A.T,1/3)),3) / 2
            elif directed_triangles_rule == 'middleman':
                triangles = np.diag(np.power(A,1/3) * np.power(A.T,1/3) * np.power(A,1/3))
            elif directed_triangles_rule == 'in':
                triangles = np.diag(matrix_power(np.power(A.T,1/3) * np.power(A,1/3),2))
            elif directed_triangles_rule == 'out':
                triangles = np.diag(matrix_power(np.power(A,1/3),2) * np.power(A.T,1/3))
            else: # 'cycle'
                triangles = np.diag(matrix_power(np.power(A,1/3),3))

        measure_dict['triangles'] = triangles
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['triangles']
        graph_type_measures[GraphBU] = ['triangles']
        graph_type_measures[GraphWD] = ['triangles']
        graph_type_measures[GraphWU] = ['triangles']
        return graph_type_measures
