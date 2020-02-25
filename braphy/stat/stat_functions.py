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
            binscenters = binscenters-dbinscenters
            binscenters = np.insert(binscenters, 0, binscenters[0]-dbinscenters)
            scounts = np.insert(scounts, 0, 0)

            for i in range(P+1):
                indices_low = np.where(scounts <= i)[0]
                indices_high = np.where(scounts >= i)[0]

                if len(indices_low) != 0 and len(indices_high) != 0:
                    q[i, n] = (binscenters[indices_low[-1]] + binscenters[indices_high[0]])/2
                else:
                    q[i, n] = np.nan
        return q

    def p_value_one_tail(res, values):
        N = np.shape(values)[1]
        M = np.shape(values)[0]

        p_single = np.ones(N)
        for n in range(N):
            res_tmp = res[n]
            values_tmp = values[:,n]

            res_tmp = res_tmp - np.mean(values_tmp)
            values_tmp = values_tmp - np.mean(values_tmp)

            if res_tmp > 0:
                p_single[n] = np.sum(values_tmp > res_tmp) / len(values_tmp)
            else:
                p_single[n] = np.sum(values_tmp < res_tmp) / len(values_tmp)
        p_single[p_single == 0] = 1/M
        p_single[np.isnan(res)] = np.nan
        return p_single

    def p_value_two_tail(res, values):
        N = np.shape(values)[1]
        M = np.shape(values)[0]

        p_double = np.ones(N)
        for n in range(N):
            res_tmp = res[n]
            values_tmp = values[:,n]

            res_tmp = res_tmp - np.mean(values_tmp)
            values_tmp = values_tmp - np.mean(values_tmp)

            p_double[n] = np.sum(np.abs(values_tmp) > np.abs(res_tmp)) / len(values_tmp)
        p_double[p_double == 0] = 1/M
        p_double[np.isnan(res)] = np.nan
        return p_double
