from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget
from braphy.atlas.brain_region import BrainRegion
from braphy.gui.gui_brain_edge import GUIBrainEdge
from braphy.gui.gui_brain_region import GUIBrainRegion
from braphy.utility.helper_functions import abs_path_from_relative, load_nv

class SlideShow3DWidget(BrainAtlasWidget):
    def __init__(self, parent = None):
        super(SlideShow3DWidget, self).__init__(parent)
        self.color = [1.0, 0.0, 2.0/3, 1.0] # pink
        self.slides = [self.set_degree, self.set_eccentricity, self.set_triangles] # add measure-functions here
        self.slide_show_timer = QtCore.QBasicTimer()
        self.step = 0
        self.delay = 5000 # milliseconds
        self.timerEvent()

    def init(self, brain_mesh_file, color):
        mesh_data = load_nv(brain_mesh_file)
        self.set_brain_mesh(mesh_data)
        self.set_locked(True)
        self.animate(True)
        self.setBrainBackgroundColor(color)
        self.change_transparency(0.3)
        self.setCameraPosition(distance = 275)
        self.set_degree()

    def add_edge(self, coords, color, radius = 1.0):
        brain_removed = False
        try:
            self.removeItem(self.brain_mesh)
            brain_removed = True
        except:
            pass
        brain_edge = GUIBrainEdge(coords[0], coords[1], color, radius)
        self.addItem(brain_edge)
        if brain_removed:
            self.addItem(self.brain_mesh)

    def get_gui_brain_edge_items(self):
        gui_brain_edge_items = []
        for item in self.items:
            if isinstance(item, GUIBrainEdge):
                gui_brain_edge_items.append(item)
        return gui_brain_edge_items

    def clear_gui_brain_edges(self):
        for item in self.get_gui_brain_edge_items():
            self.removeItem(item)

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

    def set_triangles(self): # copy this function and alter coords and edges
        self.clear_gui_brain_edges()
        self.clear_gui_brain_regions()
        coords = [[40, 45, 25],
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
                  [20, -80, 10],#
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
        brain_regions = []
        for c in coords:
            self.add_region(c, self.color, 4)
        edges = [(2,4), (2,8), (4,8), (8,9), (8,10), (9,10),
        (4,11), (8,11), (8,12), (11,12), (18, 20), (18, 24), (20, 24), (24, 25), (24, 26),
        (25, 26), (20, 27), (24, 27), (24, 28), (27, 28)] # edges between nodes
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [0.0, 0.0, 1.0, 1.0])
        edges = [(0,3), (7,8), (8,13), (16, 19), (23, 24), (24, 29)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [0.0, 1.0, 0.0, 1.0]) 
            #specify any rgb color, last digit should be 1
        edges = [(0,1), (0,2), (1,2), (16,17), (16,18), (17,18)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.color)


    
    def set_degree(self): # copy this function and alter coords and edges
        self.clear_gui_brain_edges()
        coords = [[40, 45, 25],
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
                  [20, -80, 10],#
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
        brain_regions = []
        for c in coords:
            brain_regions.append(BrainRegion(x=c[0], y=c[1], z=c[2]))
        self.init_brain_regions(brain_regions, 4, [], True, False)
        edges = [(0,2), (16,18)] # edges between nodes, regions in one brain side 0-15, other 16-
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [0.0, 0.0, 1.0, 1.0])
        edges = [(2,6), (2,7), (2,12), (2,14), (2,10), (3,9), (3,4), (3,5), (3,14), (3,13), 
        (4,10), (4,9), (4,7), (5,6), (5,7), (5,15), (5,11), (5,10), (6,9), (6,10), (6,11), 
        (6,7), (6,13), (7,12), (7,14), (7,13), (9,14), (9,15), (9,13), (10, 13), (10,12), 
        (10,15), (12,15), (13,15), (14,15), 
        (18,22), (18,23), (18,28), (18,30), (18,26), (19,25), (19,20), (19,21), (19,30), 
        (19,29), (20,26), (20,25), (20,23), (21,22), (21,23), (21,31), (21,27), (21,26),
        (22,25), (22,26), (22,27), (22,23), (22,29), (23,28), (23,30), (23,29), (25,30), 
        (25,31), (25,29), (26,29), (26,28), (26,31), (28,31), (29,31), (30,31)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [1.0, 1.0, 1.0, 1.0], 0.2) 
            #specify any rgb color, last digit should be 1
        edges = [(2,8), (8,10), (8,11), (8,14), (5,8), (1,8), (3,8), 
        (18,24), (24,26), (24,27), (24,30), (21,24), (17,24), (19, 24)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.color)


    def set_eccentricity(self): # copy this function and alter coords and edges
        self.clear_gui_brain_edges()
        coords = [[40, 45, 25],
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
                  [20, -80, 10],#end of one brain side
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
        brain_regions = []
        for c in coords:
            brain_regions.append(BrainRegion(x=c[0], y=c[1], z=c[2]))
        self.init_brain_regions(brain_regions, 4, [], True, False)
        edges = [(11,12), (8,11), (2,8), (0,2), 
        (27,28), (24, 27), (18,24), (16,18)] # edges between nodes, regions in one brain side 0-15, other 16-
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [0.0, 0.0, 1.0, 1.0])
        edges = [(1,2), (1,4), (1,9), (2,4), (2,9), (3,4), (3,5), (3,6), (3,7), 
        (4,9), (4,5), (5,6), (5,7), (6,7), (8,9), (8,10), (10,12), (11,14), (11,13), 
        (12,15), (13,14), 
        (17,18), (17,20), (17,25), (18,20), (18,25), (19,20), (19,21), (19,22), (19,23), 
        (20,25), (20,21), (21,22), (21,23), (22,23), (24,25), (24,26), (26,28), (27,30), (27,29), 
        (28,31), (29,30)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [1.0, 1.0, 1.0, 1.0], 0.2) 
            #specify any rgb color, last digit should be 1
        edges = [(8,12), (4,8), (0,4), 
        (24, 28), (20, 24), (16,20)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.color)

    def set_test(self):
        self.clear_gui_brain_edges()
        self.clear_gui_brain_regions()
        coords = [[-20, -50, 0],
                  [40, 50, 20]]
        brain_regions = []
        for c in coords:
            self.add_region(c, self.color, 4)
        self.add_edge(coords, self.color, 3.0)

    def timerEvent(self, e = None):
        if self.step >= len(self.slides):
            self.slide_show_timer.stop()
            return
        self.slide_show_timer.start(self.delay, self)
        slide = self.slides[self.step]
        slide()
        self.step += 1
        if self.step >= len(self.slides):
            self.step = 0
