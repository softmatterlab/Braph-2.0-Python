import numpy as np
import os

def abs_path_from_relative(script_file, file_relative = None):
    script_path = os.path.abspath(script_file)
    script_dir = os.path.split(script_path)[0]
    if file_relative == None:
        file_absolute = script_dir
    else:
        file_absolute = os.path.join(script_dir, file_relative)
    return file_absolute

def load_nv(filename):
    number_of_vertices = np.loadtxt(filename, max_rows = 1).astype(int).item()
    vertices = np.loadtxt(filename, skiprows = 1, max_rows = number_of_vertices)
    number_of_faces = np.loadtxt(filename, skiprows = number_of_vertices+1, max_rows = 1).astype(int).item()
    faces = np.loadtxt(filename, skiprows = number_of_vertices+2, max_rows = number_of_faces).astype(int) -1
    return {'vertices':vertices, 'faces':faces}

def list_data_types():
    data_types = []
    workflow_dir = abs_path_from_relative(__file__, '../workflows')
    files = os.listdir(workflow_dir)
    for f in files:
        if os.path.isdir(os.path.join(workflow_dir, f)) and not f.startswith('_'):
            data_types.append(f.capitalize())
    return data_types

