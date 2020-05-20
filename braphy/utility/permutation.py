import numpy as np

class Permutation():
    def permute(values_1, values_2, is_longitudinal):
        if is_longitudinal: # values are vectors
            values_1 = np.array(values_1)
            values_2 = np.array(values_2)
            n_subjects_1 = values_1.shape[0]
            values = np.concatenate((values_1, values_2))
            np.random.shuffle(values)
            permutation_1 = values[:n_subjects_1]
            permutation_2 = values[n_subjects_1:]
        else: # values are matrices
            n_subjects_1 = values_1.shape[0]
            values = np.vstack((values_1, values_2))
            np.random.shuffle(values)
            permutation_1 = values[:n_subjects_1, :]
            permutation_2 = values[n_subjects_1:, :]
        return permutation_1, permutation_2
