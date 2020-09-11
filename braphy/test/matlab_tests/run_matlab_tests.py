import numpy as np
import scipy.io as sio
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graphs.graph import Graph
from braphy.graph.measures.measure import Measure
from braphy.test.test_utility import TestUtility

def get_matlab_measure_mapping():
    # Add the name of the measures in mat ĺab here:
    mapping = {
        'degree': 'Degree',
        'avg_degree': 'DegreeAv',
        'in_degree': 'InDegree',
        'out_degree': 'OutDegree',
        'avg_in_degree': 'InDegreeAv',
        'avg_out_degree': 'OutDegreeAv',
        'strength': 'Strength',
        'avg_strength': 'StrengthAv',
        'in_strength': 'InStrength',
        'avg_in_strength': 'InStrengthAv',
        'out_strength': 'OutStrength',
        'avg_out_strength': 'OutStrengthAv',
        'assortativity': None,
        'assortativity_out_in': None,
        'assortativity_in_out': None,
        'assortativity_out_out': None,
        'assortativity_in_in': None,
        'betweenness': None,
        'distance': 'Distance',
        'path_length': 'PathLength',
        'char_path_length': 'PathLengthAv',
        'in_path_length': 'InPathLength',
        'char_in_path_length': 'InPathLengthAv',
        'out_path_length': 'OutPathLength',
        'char_out_path_length': 'OutPathLengthAv',
        'char_path_length_wsg': None,
        'closeness': None,
        'closeness_in': None,
        'closeness_out': None,
        'triangles': 'Triangles',
        'cluster': 'Clustering',
        'avg_cluster': 'ClusteringAv',
        'community_structure': None,
        'modularity': None,
        'eccentricity': None,
        'avg_eccentricity': None,
        'in_eccentricity': None,
        'avg_in_eccentricity': None,
        'out_eccentricity': None,
        'avg_out_eccentricity': None,
        'radius': None,
        'diameter': None,
        'edge_betweenness_centrality': None,
        'edge_number_distance': None,
        'global_efficiency': 'GlobalEfficiency',
        'avg_global_efficiency': 'GlobalEfficiencyAv',
        'in_global_efficiency': 'InGlobalEfficiency',
        'avg_in_global_efficiency': 'InGlobalEfficiencyAv',
        'out_global_efficiency': 'OutGlobalEfficiency',
        'avg_out_global_efficiency': 'OutGlobalEfficiencyAv',
        'local_efficiency': 'LocalEfficiency',
        'avg_local_efficiency': 'LocalEfficiencyAv',
        'in_local_efficiency': None,
        'avg_in_local_efficiency': None,
        'out_local_efficiency': None,
        'avg_out_local_efficiency': None,
        'participation': None,
        'path_transitivity': None,
        'small_worldness': None,
        'transitivity': 'Transitivity',
        'z_score': None,
        'in_z_score': None,
        'out_z_score': None
    }
    return mapping

def run_test():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    matlab_data = sio.loadmat(dir_path + '/matlab_output.mat', variable_names = ['output'])
    file_name = dir_path+'/matlab_matrix.mat'
    matrices = sio.loadmat(file_name)

    matlab_mapping = get_matlab_measure_mapping()

    graph_types = {
        'GraphBU': (False, False),
        'GraphBD': (False, True),
        'GraphWU': (True, False),
        'GraphWD': (True, True)
    }
    test = TestUtility()

    for i in range(1, len(matrices)-2):
        print('random matrix number: {}'.format(i))
        variable_name = 'matrix_{}'.format(i)
        matrix = sio.loadmat(file_name, variable_names=[variable_name])
        matrix = matrix[variable_name]
        for graph_type, graph_settings in graph_types.items():
            settings = GraphSettings(weighted = graph_settings[0], directed = graph_settings[1])
            graph = GraphFactory.get_graph(matrix, settings)
            measures_dict = graph.settings.measure_list
            for measure_class, sub_measures in measures_dict.items():
                for sub_measure in sub_measures:
                    if sub_measure == 'small_worldness':
                        continue # not yet implemented correctly
                    try:
                        measure = graph.get_measure(measure_class, sub_measure, False)
                    except:
                        print('************************')
                        print('Cannot compute {} with graph type {}'.format(sub_measure, graph_type))
                        print('************************')
                        continue

                    matlab_measure_string = matlab_mapping[sub_measure]
                    if matlab_measure_string is None:
                        continue # This measure is not available in the dictionary above.
                                 #If it is implemented in braph2, you may add it to the list.
                    matlab_measure = np.squeeze(matlab_data['output']['matrix_{}'.format(i)][0,0][graph_type][0,0][matlab_measure_string][0,0][0,0])
                    try:
                        if measure_class.dimensions()[sub_measure] == Measure.BINODAL:
                            test.assertMatrixAlmostEqual(measure, matlab_measure, 4)
                        elif measure_class.dimensions()[sub_measure] == Measure.NODAL:
                            test.assertSequenceAlmostEqual(measure.tolist(), matlab_measure.tolist(), 4)
                        else: #global
                            test.assertAlmostEqual(measure, matlab_measure, 4)
                    except:
                        print('Error at \nmatrix number: {}, measure: {}, graph type: {}'.format(i, sub_measure, graph_type))


if __name__ == "__main__":
    run_test()