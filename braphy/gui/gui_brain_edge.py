import pyqtgraph.opengl as gl
import numpy as np
import math

class GUIBrainEdge(gl.GLMeshItem):
    def __init__(self, start, end, color, radius):
        length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2 + (end[2] - start[2])**2)
        meshdata = gl.MeshData.cylinder(10, 20, radius=[radius, radius], length = length)
        super().__init__(meshdata = meshdata, shader = 'shaded', smooth = True, color = color)
        direction = [x - y for x, y in zip(end, start)]
        orthogonal_direction = [-direction[1], direction[0], 0]
        angle = np.arccos(direction[2]/(math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2))) * (180/math.pi)
        self.rotate(angle, orthogonal_direction[0], orthogonal_direction[1], orthogonal_direction[2])
        self.translate(start[0], start[1], start[2])