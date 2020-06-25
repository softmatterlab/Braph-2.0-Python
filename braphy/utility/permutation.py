import numpy as np

class Permutation():
    def permute(values_1, values_2, is_longitudinal):
        if is_longitudinal:
            values_1 = np.array(values_1)
            values_2 = np.array(values_2)
            assert values_1.shape == values_2.shape
            permutation_1 = values_1.copy()
            permutation_2 = values_2.copy()
            permutation = np.random.randint(2, len(values_1))
            permutation_1[permutation==1] = values_2[permutation==1]
            permutation_2[permutation==1] = values_1[permutation==1]
        else:
            n_subjects_1 = values_1.shape[0]
            values = np.concatenate((values_1, values_2))
            np.random.shuffle(values)
            permutation_1 = values[:n_subjects_1]
            permutation_2 = values[n_subjects_1:]
        return permutation_1, permutation_2
