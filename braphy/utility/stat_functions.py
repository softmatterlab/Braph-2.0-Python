import numpy as np
from scipy import stats, linalg

class StatFunctions():
    def false_discovery_rate(p_values, q = 0.05):
        if q < 0:
            q = 0
        elif q > 1:
            q = 1

        x = np.arange(len(p_values))/len(p_values)
        p_values = np.sort(p_values)

        index = np.sum(p_values <= q*x)
        if index > 0:
            r = p_values[index]
        else:
            r = 0
        return r

    def quantiles(values, P = 100):
        assert len(values) > 0, 'No elements in values'
        if len(values.shape) == 1:
            return StatFunctions.quantiles_1d(values, P)
        elif len(values.shape) == 2:
            return StatFunctions.quantiles_2d(values, P)
        elif len(values.shape) == 3:
            return StatFunctions.quantiles_3d(values, P)


    def quantiles_1d(values, P = 100):
        # NOTE the implementation of percentile in python might differ from quantile in matlab
        percentiles = []
        for k in range(P):
            percentiles.append(np.percentile(values, k*100/(P-1)))
        Q = np.array(percentiles)
        return Q

    def quantiles_2d(values, P = 100):
        Q = []
        for i in range(values.shape[0]):
            current_values = values[i].copy()
            # NOTE the implementation of percentile in python might differ from quantile in matlab
            percentiles = []
            for k in range(P):
                percentiles.append(np.percentile(current_values, k*100/(P-1)))
            Q.append(percentiles)
        Q = np.array(Q)
        return Q

    def quantiles_3d(values, P = 100):
        Q = np.zeros([values.shape[0], values.shape[1],P])
        for i in range(values.shape[0]):
            for j in range(values.shape[1]):
                current_values = values[i,j,:].copy()
                # NOTE the implementation of percentile in python might differ from quantile in matlab
                percentiles = []
                for k in range(P):
                    percentiles.append(np.percentile(current_values, k*100/(P-1)))
                Q[i,j,:] = np.array(percentiles)
        Q = np.squeeze(Q)
        return Q


    def p_value(observed_difference, random_differences, single = True):
        assert len(np.shape(observed_difference)) == len(np.shape(random_differences)) - 1
        M = random_differences.size
        if len(np.shape(observed_difference)) == 0:
            return StatFunctions.p_value_scalar(observed_difference, random_differences, single)
        elif len(np.shape(observed_difference)) == 1:
            return StatFunctions.p_value_vector(observed_difference, random_differences, single)
        elif len(np.shape(observed_difference)) == 2:
            return StatFunctions.p_value_matrix(observed_difference, random_differences, single)

    def p_value_scalar(observed_difference, random_differences, single):
        M = len(random_differences) + 1
        normalized_observed_difference = observed_difference - np.mean(random_differences)
        normalized_random_differences = random_differences - np.mean(random_differences)
        if single:
            if normalized_observed_difference > 0:
                p_value = (np.sum(normalized_random_differences > normalized_observed_difference) + 1) / M
            else:
                p_value = (np.sum(normalized_random_differences < normalized_observed_difference) + 1) / M
        else:
            p_value = (np.sum(np.abs(normalized_random_differences) > np.abs(normalized_observed_difference)) + 1) / M
        return p_value

    def p_value_vector(observed_difference, random_differences, single):
        N = np.shape(random_differences)[-1]
        p_value = np.ones(N)
        for n in range(N):
            p_value[n] = StatFunctions.p_value_scalar(observed_difference[n], random_differences[:,n], single)
        return p_value

    def p_value_matrix(observed_difference, random_differences, single):
        N = np.shape(random_differences)[-1]
        p_value = np.ones([N, N])
        for n in range(N):
            p_value[n,:] = StatFunctions.p_value_vector(observed_difference[:,n], random_differences[:,:,n], single)
        return p_value

    def bonferroni(p_values, p):
        # calculates the Bonferroni correction for p-values. p is the starting p-value.
        r = p / len(p_values)
        return r

    def correlation(data, correlation_type):
        correlation_type = correlation_type.replace(' ', '_')
        corr = np.zeros((data.shape[1], data.shape[1]), dtype=np.float)
        try:
            correlation_function = eval('StatFunctions.correlation_{}'.format(correlation_type))
            corr = correlation_function(data)
        except Exception as e:
            print('Correlation function {} not implemented'.format(correlation_type))
            print(e)
        return corr

    def correlation_pearson(data):
        return np.corrcoef(data)

    def correlation_spearman(data):
        rank = np.argsort(data)
        return np.corrcoef(rank)

    def correlation_kendall(data):
        correlation = np.zeros((data.shape[0], data.shape[0]))
        for i in range(data.shape[0]):
            for j in range(data.shape[0]):
                correlation[i, j] = stats.kendalltau(data[i], data[j])[0]
        return correlation

    def correlation_partial_pearson(data):
        data = data.T
        data = np.asarray(data)
        nodes = data.shape[1]
        correlation = np.zeros((nodes, nodes), dtype=np.float)
        for i in range(nodes):
            correlation[i, i] = 1
            for j in range(i+1, nodes):
                idx = np.ones(nodes, dtype=np.bool)
                idx[i] = False
                idx[j] = False
                beta_i = linalg.lstsq(data[:, idx], data[:, j])[0]
                beta_j = linalg.lstsq(data[:, idx], data[:, i])[0]
                res_j = data[:, j] - data[:, idx].dot(beta_i)
                res_i = data[:, i] - data[:, idx].dot(beta_j)
                corr = stats.pearsonr(res_i, res_j)[0]
                correlation[i, j] = corr
                correlation[j, i] = corr
        return correlation

    def correlation_partial_spearman(data):
        data = data.T
        data = np.asarray(data)
        nodes = data.shape[1]
        correlation = np.zeros((nodes, nodes), dtype=np.float)
        for i in range(nodes):
            correlation[i, i] = 1
            for j in range(i+1, nodes):
                idx = np.ones(nodes, dtype=np.bool)
                idx[i] = False
                idx[j] = False
                beta_i = linalg.lstsq(data[:, idx], data[:, j])[0]
                beta_j = linalg.lstsq(data[:, idx], data[:, i])[0]
                res_j = data[:, j] - data[:, idx].dot(beta_i)
                res_i = data[:, i] - data[:, idx].dot(beta_j)
                corr = stats.spearmanr(res_i, res_j)[0]
                correlation[i, j] = corr
                correlation[j, i] = corr
        return correlation
