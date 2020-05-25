import numpy as np

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

    # TODO - check with numpy.quantile
    def quantiles(values, P = 100):
        N = np.size(values, 1)
        M = np.size(values, 0)

        q = np.zeros([P+1, N])

        C = 10*P;
        for n in range(N):
            counts, binscenters = np.histogram(values[:,n], C)
            binscenters = binscenters[:-1] + np.diff(binscenters)/2

            scounts = P*np.cumsum(counts, 0)/np.sum(counts)

            dbinscenters = (binscenters[1] - binscenters[0])/2
            binscenters = binscenters+dbinscenters
            binscenters = np.insert(binscenters, 0, binscenters[0]-2*dbinscenters)
            scounts = np.insert(scounts, 0, 0)

            for i in range(P+1):
                indices_low = np.where(scounts <= i)[0]
                indices_high = np.where(scounts >= i)[0]

                if len(indices_low) != 0 and len(indices_high) != 0:
                    q[i, n] = (binscenters[indices_low[-1]] + binscenters[indices_high[0]])/2
                else:
                    q[i, n] = np.nan
        return q

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