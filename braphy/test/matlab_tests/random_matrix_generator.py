
import numpy as np
import scipy.io as sio
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def generate_test_data():
    file_name = 'random_matrices'
    number_of_matrices = 100
    matrix_size = 100
    matrix_dict = {}
    for i in range(number_of_matrices):
        random_matrix = 2 * np.random.rand(matrix_size,matrix_size) - 1 # generate random matrix in range (-1, 1)
        matrix_name = 'matrix_{}'.format(i+1)
        matrix_dict[matrix_name] = random_matrix

    dir_path = os.path.dirname(os.path.realpath(__file__))
    sio.savemat(dir_path + '/matlab_matrix.mat', matrix_dict)

if __name__ == "__main__":
    generate_test_data()
