from braphy.graph.measures.measure import Measure
from braphy.graph.measures.measure_triangles import MeasureTriangles
from braphy.graph.measures.measure_degree import MeasureDegree
from braphy.graph.graphs import *
import numpy as np
import copy
from numpy.linalg import matrix_power, multi_dot

class MeasureCluster(Measure):

    def dimensions():
        d = {}
        d['cluster'] = Measure.NODAL
        d['avg_cluster'] = Measure.GLOBAL
        return d

    def get_description():

        description = {}
        description['cluster'] = 'The clustering coefficient is the fraction of triangles around a node. ' +\
                                 'It is equivalent to the fraction of a node''s neighbors that are neighbors of each other.'

        description['avg_cluster'] = 'The clustering coefficient of a graph is '+\
                                     'the average of the clustering coefficients of its nodes.'

        return description

    def compute_measure(graph):
        measure_dict = {}
        triangles = graph.get_measure(MeasureTriangles, 'triangles', save = False)

        if graph.is_directed():
            A = graph.A.copy()
            np.fill_diagonal(A, 0)
            in_degree = graph.get_measure(MeasureDegree, 'in_degree', save = False)
            out_degree = graph.get_measure(MeasureDegree, 'out_degree', save = False)
            in_degree = in_degree.astype(float)
            out_degree = out_degree.astype(float)

            in_degree[triangles==0] = np.inf
            out_degree[triangles==0] = np.inf
            # 'middleman/cycle rule'
            cluster = triangles/(out_degree*in_degree - np.diag(matrix_power(A, 2)))

        else:
            degree = graph.get_measure(MeasureDegree, 'degree', save = False)
            if graph.is_binary(): #BU
                cluster = np.zeros(len(triangles))
                indices = np.argwhere((triangles!=0) & (degree>1)).flatten()
                cluster[indices] = 2*triangles[indices]/(degree[indices]*(degree[indices]-1))

            else: #WU
                degree = degree.astype(float)
                degree[triangles==0] = np.inf

                cluster = 2*triangles/(degree*(degree-1))

        measure_dict['cluster'] = cluster
        measure_dict['avg_cluster'] = np.mean(cluster)
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['cluster', 'avg_cluster']
        graph_type_measures[GraphBU] = ['cluster', 'avg_cluster']
        graph_type_measures[GraphWD] = ['cluster', 'avg_cluster']
        graph_type_measures[GraphWU] = ['cluster', 'avg_cluster']
        return graph_type_measures
