from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph.opengl import GLViewWidget
from PyQt5.QtGui import QColor
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget
from braphy.atlas.brain_region import BrainRegion
from braphy.gui.gui_brain_edge import GUIBrainEdge
from braphy.gui.gui_brain_region import GUIBrainRegion
from braphy.utility.file_utility import abs_path_from_relative, load_nv

brain_mesh_file_name = "../meshes/BrainMesh_ICBM152.nv"
brain_mesh_file = abs_path_from_relative(__file__, brain_mesh_file_name)

class SlideShow3DWidget(BrainAtlasWidget):
    def __init__(self, parent = None):
        super(SlideShow3DWidget, self).__init__(parent)
        self.pink = [1.0, 0.0, 2.0/3, 1.0]
        self.white = [1.0, 1.0, 1.0, 1.0]
        self.blue = [0.0, 0.0, 1.0, 1.0]
        self.green = [0.0, 1.0, 0.0, 1.0]
        self.yellow = [1.0, 1.0, 0.0, 1.0]
        self.red = [1.0, 0.0, 0.0, 1.0]
        self.purple = [1.0, 0.0, 1.0, 1.0]
        self.coords = [[40, 45, 25],
                       [25, 35, 23],
                       [40, 35, 5],
                       [30, 32, 45],
                       [45, -5, 40],
                       [35, -10, 45],
                       [10, 5, 65],
                       [35, -25, 60],
                       [50, -25, 0],
                       [45, 5, -20],
                       [52, -25, -25], 
                       [48, -50, -10],
                       [30, -45, 5], 
                       [35, -48, 40],
                       [25, -90, 0],
                       [20, -80, 10], #other side of the brain below
                       [-40, 45, 25],
                       [-25, 35, 23],
                       [-40, 35, 5],
                       [-30, 32, 45],
                       [-45, -5, 40],
                       [-35, -10, 45],
                       [-10, 5, 65],
                       [-35, -25, 60],
                       [-50, -25, 0],
                       [-45, 5, -20],
                       [-52, -25, -25], 
                       [-48, -50, -10],
                       [-30, -45, 5], 
                       [-35, -48, 40],
                       [-25, -90, 0],
                       [-20, -80, 10]]
        self.slides = [self.set_degree, self.set_strength, self.set_eccentricity,
                       self.set_global_efficiency, self.set_path_length, self.set_triangles,
                       self.set_clustering, self.set_participation, self.set_betweenness,
                       self.set_modularity, self.set_zscore]

    def init(self, color):
        mesh_data = load_nv(brain_mesh_file)
        self.set_brain_mesh(mesh_data)
        self.set_locked(True)
        self.animate(True)
        self.set_brain_background_color(color)
        self.change_transparency(0.3)
        self.setCameraPosition(distance = 275)
        self.set_degree()

    def paintGL(self, *args, **kwds):
        GLViewWidget.paintGL(self, *args, **kwds)
        self.qglColor(QColor("k"))
        for edge in self.get_gui_brain_edge_items():
            if edge.label:
                pos = edge.get_center_pos()
                self.renderText(pos[0], pos[1], pos[2], edge.label)

    def add_region(self, coord, color, radius):
        brain_removed = False
        try:
            self.removeItem(self.brain_mesh)
            brain_removed = True
        except:
            pass
        brain_region = BrainRegion(x = coord[0], y = coord[1], z = coord[2])
        gui_brain_region = GUIBrainRegion(brain_region, radius, False, color, None)
        self.addItem(gui_brain_region)
        if brain_removed:
            self.addItem(self.brain_mesh)

    def clear_animation(self):
        self.clear_gui_brain_edges()
        self.clear_gui_brain_regions()

    def set_triangles(self):
        description = 'Number of TRIANGLES around a node is the number of neighbors of that node '\
                      'that are neightbors to each other.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        for c in coords:
            self.add_region(c, self.white, 3) 
        coords_diff_regions = [coords[0], coords[16]]
        for c in coords_diff_regions:
            self.add_region(c, self.blue, 5)
        coords_diff_regions = [coords[8], coords[24]]
        for c in coords_diff_regions:
            self.add_region(c, self.pink, 5)
        edges = [(2,4), (2,8), (4,8), (8,9), (8,10), (9,10),
        (4,11), (8,11), (8,12), (11,12), (18, 20), (18, 24), (20, 24), (24, 25), (24, 26),
        (25, 26), (20, 27), (24, 27), (24, 28), (27, 28)]
        # regions in one brain side 0-15, other 16-31
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.pink, 0.7)
        edges = [(0,3), (7,8), (8,13), (16, 19), (23, 24), (24, 29)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.3) 
        edges = [(0,1), (0,2), (1,2), (16,17), (16,18), (17,18)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue, 0.7)
        return description

    def set_clustering(self):
        description = 'CLUSTERING coefficient is the fraction of triangles around a node. It is '\
                      'equivalent to the fraction of the neighbors of the node that are neighbors '\
                      'of each other.'
        self.set_triangles()
        return description

    def set_degree(self): 
        description = 'DEGREE of a node is the number of edges connected to the node. Connection '\
                      'weights are ignored in calculations.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        for c in coords:
            self.add_region(c, self.white, 3)
        blue_coords = [coords[0], coords[16]]
        for c in blue_coords:
            self.add_region(c, self.blue, 5)
        red_coords = [coords[8], coords[24]]
        for c in red_coords:
            self.add_region(c, self.pink, 5)

        edges = [(0,2), (16,18)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue, 0.7)
        edges = [(2,6), (2,7), (2,14), (2,10), (3,4), (3,5), (3,14), 
        (4,9), (5,6), (5,7), (5,11), (5,10), (6,9), (6,10), (6,11), 
        (6,13), (7,14), (7,13), (9,14), (9,13), (10,12), 
        (10,15), (12,15), (13,15), (14,15), 
        (18,22), (18,23), (18,30), (18,26), (19,20), (19,21), (19,30), 
        (20,25), (21,22), (21,23), (21,27), (21,26),
        (22,25), (22,26), (22,27), (22,29), (23,30), (23,29), (25,30), 
        (25,29), (26,28), (26,31), (28,31), (29,31), (30,31)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.3) 
        edges = [(2,8), (8,10), (8,11), (8,7), (5,8), (1,8), (3,8), 
        (18,24), (24,26), (24,27), (24,23), (21,24), (17,24), (19, 24)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.pink, 0.7)
        return description

    def set_strength(self): 
        description = 'STRENGTH of a node is the sum of the weights of the edges connected to the '\
                      'node. Number of connections are ignored in calculations.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        for c in coords:
            self.add_region(c, self.white, 3)
        red_coords = [coords[0], coords[16]]
        for c in red_coords:
            self.add_region(c, self.pink, 5)
        blue_coords = [coords[8], coords[24]]
        for c in blue_coords:
            self.add_region(c, self.blue, 5)
        edges = [(0,2), (16,18)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.pink, 0.7)
        edges = [(2,6), (2,7), (2,14), (2,10), (3,4), (3,5), (3,14), 
        (4,9), (5,6), (5,7), (5,11), (5,10), (6,9), (6,10), (6,11), 
        (6,13), (7,14), (7,13), (9,14), (9,13), (10,12), 
        (10,15), (12,15), (13,15), (14,15), 
        (18,22), (18,23), (18,30), (18,26), (19,20), (19,21), (19,30), 
        (20,25), (21,22), (21,23), (21,27), (21,26),
        (22,25), (22,26), (22,27), (22,29), (23,30), (23,29), (25,30), 
        (25,29), (26,28), (26,31), (28,31), (29,31), (30,31)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.3) 
        edges = [(2,8), (8,10), (8,7), (5,8), (1,8), (3,8), 
        (18,24), (24,26), (24,23), (21,24), (17,24), (19, 24)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue, 0.7)
        edges = [(8,11),
                (24,27)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue, 0.7)
        return description

    def set_eccentricity(self): 
        description = 'ECCENTRICITY of a node is the maximal shortest path length between that '\
                      'node and any other node. If more than one path exist between a node and '\
                      'other node, the shortest path is chosen (red path in the figure).'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        for c in coords:
            self.add_region(c, self.white, 3)
        green_coords = [coords[0], coords[16], coords[12], coords[28]]
        for c in green_coords:
            self.add_region(c, self.green, 5)
        edges = [(11,12), (8,11), (2,8), (0,2), 
        (27,28), (24, 27), (18,24), (16,18)] 
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue)
        edges = [(1,2), (1,4), (1,9), (2,4), (2,9), (3,4), (3,5), (3,6), (3,7), 
        (4,9), (4,5), (5,6), (5,7), (6,7), (8,9), (8,10), (10,12), (11,14), (11,13), 
        (12,15), (13,14), 
        (17,18), (17,20), (17,25), (18,20), (18,25), (19,20), (19,21), (19,22), (19,23), 
        (20,25), (20,21), (21,22), (21,23), (22,23), (24,25), (24,26), (26,28), (27,30), (27,29), 
        (28,31), (29,30)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.3) 
        edges = [(8,12), (4,8), (0,4), (24, 28), (20, 24), (16,20)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.pink, 0.7)
        return description

    def set_path_length(self):
        description = 'PATH LENGTH of a node is the average path length from that note to all '\
                      'other nodes. If more than one path exist between a node and other node, '\
                      'the shortest path is chosen (red path in the figure).'
        self.set_eccentricity()
        return description

    def set_global_efficiency(self):
        description = 'GLOBAL EFFICIENCY is the average inverse shortest path length in the '\
                      'graph. It is inversely related to the characteristic path length. If more '\
                      'than one path exist between a node and other node, the shortest path is '\
                      'chosen (red path in the figure).'
        self.set_eccentricity()
        return description

    def set_participation(self):
        description = 'PARTICIPATION coefficient compares the number of links of a node has with '\
                      'nodes of other cluster to the number of links within its cluster. Nodes '\
                      'with a high participation coefficient (known as connector hubs) are '\
                      'connected to many clusters and are likely to facilitate global '\
                      'intermodular integration.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        greens = [8,10,11,12,13,15,
                  24,26,27,28,29,31]
        green_coords = [coords[i] for i in greens]
        for c in green_coords:
            self.add_region(c, self.green, 3)
        reds = [0,1,2,9,
                16,17,18,25]
        red_coords = [coords[i] for i in reds]
        for c in red_coords:
            self.add_region(c, self.pink, 3)
        blues = [3,5,6,7,
                 19,21,22,23]
        blue_coords = [coords[i] for i in blues]
        for c in blue_coords:
            self.add_region(c, self.blue, 3)
        yellow_coords = [coords[4], coords[20]]
        for c in yellow_coords:
            self.add_region(c, self.yellow, 5)
        purple_coords = [coords[14], coords[30]]
        for c in purple_coords:
            self.add_region(c, self.purple, 5)
        edges = [(3,5), (3,6), (3,7), (5,6), (5,7), (6,7), 
        (19,21), (19,22), (19,23), (21,22), (21,23), (22,23)] 
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue, 0.7)
        edges = [(8,10), (8,11), (8,12), (10,11), (10,12), (10,13), (11,12), (11,13), (11,14), 
        (12,13), (12, 15), (13,15), (14,15), 
        (24,26), (24,27), (24,28), (26,27), (26,28), (26,29), (27,28), (27,29), (27,30), 
        (28,29), (28,31), (29,31), (30,31)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.green, 0.7) 
        edges = [(0,1), (0,2), (0,4), (1,2), (1,4), (1,9), (2,4), (2,9), (4,9), 
        (16,17), (16,18), (16,20), (17,18), (17,20), (17,25), (18,20), (18,25), (20,25)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.pink, 0.7)
        edges = [(0,7), (3,4), (2,8), (4,8), (8,9), 
        (16,23), (19,20), (18,24), (20,24), (24,25)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.3) 
        return description

    def set_modularity(self):
        description = 'MODULARITY is a statistic that quantifies the degree to which the graph '\
                      'may be subdivided into clearly delineated groups.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        greens = [8,10,11,12,13,14,15,
                  24,26,27,28,29,30,31]
        green_coords = [coords[i] for i in greens]
        for c in green_coords:
            self.add_region(c, self.green, 3)
        reds = [0,1,2,4,9,
                16,17,18,20,25]
        red_coords = [coords[i] for i in reds]
        for c in red_coords:
            self.add_region(c, self.pink, 3)
        blues = [3,5,6,7,
                 19,21,22,23]
        blue_coords = [coords[i] for i in blues]
        for c in blue_coords:
            self.add_region(c, self.blue, 3)
        edges = [(3,5), (3,6), (3,7), (5,6), (5,7), (6,7), 
        (19,21), (19,22), (19,23), (21,22), (21,23), (22,23),
        (8,10), (8,11), (8,12), (10,11), (10,12), (10,13), (11,12), (11,13), (11,14), 
        (12,13), (12, 15), (13,15), (14,15), 
        (24,26), (24,27), (24,28), (26,27), (26,28), (26,29), (27,28), (27,29), (27,30), 
        (28,29), (28,31), (29,31), (30,31),
        (0,1), (0,2), (0,4), (1,2), (1,4), (1,9), (2,4), (2,9), (4,9), 
        (16,17), (16,18), (16,20), (17,18), (17,20), (17,25), (18,20), (18,25), (20,25),
        (0,7), (3,4), (2,8), (4,8), (8,9), 
        (16,23), (19,20), (18,24), (20,24), (24,25)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.7) 
        return description

    def set_betweenness(self):
        description = 'BETWEENNESS CENTRALITY of a node is the fraction of all shortest paths in '\
                      'the graph that contain a given node. Nodes with high values of betweenness '\
                      'centrality participate in a large number of shortest paths.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        for c in coords:
            self.add_region(c, self.white, 3)
        red_coords = [coords[8], coords[24]]
        for c in red_coords:
            self.add_region(c, self.red, 5)
        blue_coords = [coords[13], coords[29]]
        for c in blue_coords:
            self.add_region(c, self.blue, 5)
        edges = [(3,5), (3,6), (3,7), (5,6), (5,7), (6,7), 
        (19,21), (19,22), (19,23), (21,22), (21,23), (22,23),
        (8,10), (8,11), (8,12), (10,11), (10,12), (10,13), (11,12), (11,13), (11,14), 
        (12,13), (12, 15), (13,15), (14,15), 
        (24,26), (24,27), (24,28), (26,27), (26,28), (26,29), (27,28), (27,29), (27,30), 
        (28,29), (28,31), (29,31), (30,31),
        (0,1), (0,2), (0,4), (1,2), (1,4), (1,9), (2,4), (2,9), (4,9), 
        (16,17), (16,18), (16,20), (17,18), (17,20), (17,25), (18,20), (18,25), (20,25),
        (0,7), (3,4), (2,8), (4,8), (8,9), 
        (16,23), (19,20), (18,24), (20,24), (24,25)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.7) 
        return description

    def set_zscore(self):
        description = 'Within-module degree Z-SCORE of a node shows how well connected a node is '\
                      'in a given cluster by comparing the degree of the node in that cluster to '\
                      'the average degree of all nodes in the same cluster. This measure requires '\
                      'a previously determined community structure.'
        self.clear_animation()
        coords = self.coords
        brain_regions = []
        greens = [8,10,11,12,13,14,15,
                  24,26,27,28,29,30,31]
        green_coords = [coords[i] for i in greens]
        for c in green_coords:
            self.add_region(c, self.green, 3)
        reds = [0,1,2,4,9,
                16,17,18,20,25]
        red_coords = [coords[i] for i in reds]
        for c in red_coords:
            self.add_region(c, self.pink, 3)
        blues = [3,5,6,7,
                 19,21,22,23]
        blue_coords = [coords[i] for i in blues]
        for c in blue_coords:
            self.add_region(c, self.blue, 3)
        yellows = [8,14,
                  24,30]
        yellow_coords = [coords[i] for i in yellows]
        for c in yellow_coords:
            self.add_region(c, self.yellow, 5)
        purple_coords = [coords[13], coords[29]]
        for c in purple_coords:
            self.add_region(c, self.purple, 5)

        edges = [(3,5), (3,6), (3,7), (5,6), (5,7), (6,7), 
        (19,21), (19,22), (19,23), (21,22), (21,23), (22,23)] 
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.blue, 0.7)
        edges = [(8,10), (8,11), (8,12), (10,11), (10,12), (10,13), (11,12), (11,13), (11,14), 
        (12,13), (12, 15), (13,15), (14,15), 
        (24,26), (24,27), (24,28), (26,27), (26,28), (26,29), (27,28), (27,29), (27,30), 
        (28,29), (28,31), (29,31), (30,31)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.green, 0.7) 
        edges = [(0,1), (0,2), (0,4), (1,2), (1,4), (1,9), (2,4), (2,9), (4,9), 
        (16,17), (16,18), (16,20), (17,18), (17,20), (17,25), (18,20), (18,25), (20,25)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.pink, 0.7)
        edges = [(0,7), (3,4), (2,8), (4,8), (8,9), 
        (16,23), (19,20), (18,24), (20,24), (24,25)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.white, 0.3) 
        return description

    def set_test(self):
        description = 'test'
        self.clear_animation()
        coords = [[-20, -50, 0],
                  [40, 50, 20]]
        brain_regions = []
        for c in coords:
            self.add_region(c, self.pink, 4)
        self.add_edge(coords, self.pink, 3.0, label = 'HEJ')
        return description
