import numpy as np

def divide_without_warning(a, b):
    b = np.array(b) # in case b is a scalar
    nan_mask = np.isnan(b)
    inf_mask = np.isinf(b)
    zero_mask = b == 0
    b[nan_mask | inf_mask | zero_mask] = 1
    c = np.divide(a, b)
    c[nan_mask] = np.nan
    c[inf_mask] = 0
    c[zero_mask & (np.sign(c) == 1)] = np.inf
    c[zero_mask & (np.sign(c) == -1)] = -np.inf
    c[zero_mask & (np.sign(c) == 0)] = np.nan
    return c

def multiply_without_warning(a, b):
    a = np.array(a) # in case a is a scalar
    b = np.array(b)
    inf_mask_a = np.isinf(a)
    inf_mask_b = np.isinf(b)
    a[inf_mask_a] = np.sign(a)[inf_mask_a]
    b[inf_mask_b] = np.sign(b)[inf_mask_b]
    c = a * b
    c[inf_mask_a & (np.sign(c) == 1)] = np.inf
    c[inf_mask_a & (np.sign(c) == -1)] = -np.inf
    c[inf_mask_a & (np.sign(c) == 0)] = np.nan

    c[inf_mask_b & (np.sign(c) == 1)] = np.inf
    c[inf_mask_b & (np.sign(c) == -1)] = -np.inf
    c[inf_mask_b & (np.sign(c) == 0)] = np.nan
    return c

def accumarray(subs, val, size = np.nan):
    if np.isnan(size).any():
        size = [np.max(subs) + 1, 1 if subs.ndim == 1 else subs.shape[1]]
    if np.isscalar(val):
        val = np.array([val]*(np.max(subs) + 1))
    output = np.zeros(size)
    for val_index, output_index in enumerate(subs):
        if not np.isscalar(output_index):
            output_index = tuple(output_index)
        output[output_index] = output[output_index] + val[val_index]
    return output

def equal_around(a, b, decimals = 3):
    if np.isscalar(a) != np.isscalar(b):
        return False
    round_a = np.around(a, decimals)
    round_b = np.around(b, decimals)
    if np.isscalar(a):
        return round_a == round_b
    else:
        return np.array_equal(round_a, round_b)

def float_to_string(f, number_of_decimals = 6):
    try:
        f = float(f)
    except:
        raise ValueError('Input to the function float_to_string must be a single float value. Current input is {} of type {}.'.format(f, type(f)))
    s = format(f, '.{}f'.format(number_of_decimals)).rstrip('0')
    if s[-1] == '.':
        s += '0'
    return s

def float_to_string_fix_decimals(f, number_of_decimals = 2):
    f = round(f, number_of_decimals)
    s = format(f, '.' + str(number_of_decimals) + 'f')
    return s
