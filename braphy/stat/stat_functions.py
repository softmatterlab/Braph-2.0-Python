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
