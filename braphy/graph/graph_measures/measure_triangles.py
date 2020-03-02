from braphy.graph.graph_measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy
from numpy.linalg import matrix_power, multi_dot

class MeasureTriangles(Measure):

    def get_description():
        description = {}
        description['triangles'] = 'The number of triangles around a node is the numbers of couples of ' +\
                                    'node neighbors that are connected.'
        return description

    def compute_measure(graph):
        A = graph.A.copy()
        np.fill_diagonal(A, 0)

        if graph.is_undirected() and graph.is_binary():
            A3 = matrix_power(A, 3)
            triangles = 0.5*np.diag(A3)

        elif graph.is_directed() and graph.is_binary():
            triangles = np.zeros(len(A))
            for u in range(0,len(A)):
                nodes_out = np.where(A[u,:])
                nodes_in = np.transpose(np.where(A[:,u]))
                if len(nodes_out) and len(nodes_in):
                    triangles[u] = sum(sum(A[nodes_out,nodes_in]))

        elif graph.is_directed() and graph.is_weighted():
            triangles = np.zeros(len(A))
            for u in range(0,len(A)):
                nodes_out = np.where(A[u,:])
                nodes_in = np.transpose(np.where(A[:,u]))
                if len(nodes_out) and len(nodes_in):
                    out_flow = np.power(A[u,nodes_out],1/3)
                    neighbour_flow = np.transpose(np.power(A[nodes_out, nodes_in],1/3))
                    in_flow = np.power(A[nodes_in,u],1/3)
                    flow_sum = sum(sum(multi_dot([out_flow, neighbour_flow, in_flow])))
                    triangles[u] = 0.5*flow_sum

        else:
            A_power = matrix_power(np.power(A,1/3),3)
            triangles = 0.5*np.diag(A_power)

        graph.measure_dict[MeasureTriangles]['triangles'] = triangles

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['triangles']
        graph_type_measures[GraphBU] = ['triangles']
        graph_type_measures[GraphWD] = ['triangles']
        graph_type_measures[GraphWU] = ['triangles']
        return graph_type_measures
