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
        self.slides = [self.set_triangles, self.set_test] # add measure-functions here
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
        self.set_triangles()

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
