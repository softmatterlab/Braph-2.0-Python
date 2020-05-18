from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget
from braphy.atlas.brain_region import BrainRegion
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

    def set_triangles(self): # copy this function and alter coords and edges
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
        coords = [[-20, -50, 0],
                  [40, 50, 20]]
        brain_regions = []
        for c in coords:
            brain_regions.append(BrainRegion(x=c[0], y=c[1], z=c[2]))
        self.init_brain_regions(brain_regions, 4, [], True, False)
        self.add_edge(coords, self.color)

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
