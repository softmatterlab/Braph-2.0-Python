import numpy as np
import os
import subprocess

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

def abs_path_from_relative(script_file, file_relative = None):
    script_path = os.path.abspath(script_file)
    script_dir = os.path.split(script_path)[0]
    if file_relative == None:
        file_absolute = script_dir
    else:
        file_absolute = os.path.join(script_dir, file_relative)
    return file_absolute

def get_version_info():
    try:
        v = subprocess.check_output(["git", "log", "-1", "--date=short", "--pretty=format:'%ad.%h'"]).decode('ascii').replace("'","")
    except:
        v = "UNKNOWN"
    return v

def load_nv(filename):
    number_of_vertices = np.loadtxt(filename, max_rows = 1).astype(int).item()
    vertices = np.loadtxt(filename, skiprows = 1, max_rows = number_of_vertices)
    number_of_faces = np.loadtxt(filename, skiprows = number_of_vertices+1, max_rows = 1).astype(int).item()
    faces = np.loadtxt(filename, skiprows = number_of_vertices+2, max_rows = number_of_faces).astype(int) -1
    return {'vertices':vertices, 'faces':faces}

class ListManager:

    def check_bounds(lst, i, j):
        assert i >= 0 and i < len(lst)
        assert j >= 0 and j < len(lst)

    def replace(lst, i, item):
        lst[i] = item

    def swap(lst, i, j):
        ListManager.check_bounds(lst, i, j)
        spam = lst[i]
        lst[i] = lst[j]
        lst[j] = spam

    def move_to(lst, i, j):
        ListManager.check_bounds(lst, i, j)
        spam = lst[i]
        del lst[i]
        lst.insert(j, spam)

    def add_above(lst, indices, obj_constructor):
        for i in range(len(indices) - 1, -1, -1):
            lst.insert(indices[i], obj_constructor())
        indices = indices + np.array(range(1, len(indices) + 1))
        added = indices - 1
        return indices, added

    def add_below(lst, indices, obj_constructor):
        for i in range(len(indices) - 1, -1, -1):
            lst.insert(indices[i] + 1, obj_constructor())
        indices = indices + np.array(range(0, len(indices)))
        added = indices + 1
        return indices, added

    def move_up(lst, indices):
        if len(indices) > 0:
            first_index_to_process = 0
            unprocessable_length = 0
            while True:
                if (first_index_to_process >= len(lst)):
                    break
                if (first_index_to_process >= len(indices)):
                    break
                if (indices[first_index_to_process] != unprocessable_length):
                    break
                first_index_to_process = first_index_to_process + 1
                unprocessable_length = unprocessable_length + 1

            for i in range(first_index_to_process, len(indices)):
                ListManager.swap(lst, indices[i], indices[i] - 1)
                indices[i] = indices[i] - 1
        return indices

    def move_down(lst, indices):
        if (len(indices) > 0) & (len(indices) < len(lst)):
            last_index_to_process = len(indices) - 1
            unprocessable_length = len(lst) - 1
            while (last_index_to_process >= 0) \
                  & (indices[last_index_to_process] == unprocessable_length):
                last_index_to_process = last_index_to_process - 1
                unprocessable_length = unprocessable_length - 1

            for i in range(last_index_to_process, -1, -1):
                ListManager.swap(lst, indices[i], indices[i] + 1)
                indices[i] = indices[i] + 1
        return indices

    def move_to_top(lst, indices):
        if len(indices) > 0:
            for i in range(len(indices)):
                ListManager.move_to(lst, indices[i], i)
            indices = np.arange(0, len(indices))
        return indices

    def move_to_bottom(lst, indices):
        if len(indices) > 0:
            for i in range(len(indices) - 1, -1, -1):
                ListManager.move_to(lst, indices[i], len(lst) - (len(indices) - i))
            indices = np.arange(len(lst) - len(indices), len(lst))
        return indices
