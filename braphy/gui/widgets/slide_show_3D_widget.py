from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget
from braphy.atlas.brain_region import BrainRegion
from braphy.utility.helper_functions import abs_path_from_relative, load_nv

class SlideShow3DWidget(BrainAtlasWidget):
    def __init__(self, parent = None):
        super(SlideShow3DWidget, self).__init__(parent)
        self.color = [1.0, 0.0, 2.0/3, 1.0] # pink
        self.slides = [self.set_strength, self.set_clustering] # add measure-functions here
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
        self.set_strength()

    def set_strength(self): # copy this function and alter coords and edges
        self.clear_gui_brain_edges()
        coords = [[10, 20, 30],
                  [40, 50, 20],
                  [0, 0, 0],
                  [-60, 50, -10]]
        brain_regions = []
        for c in coords:
            brain_regions.append(BrainRegion(x=c[0], y=c[1], z=c[2]))
        self.init_brain_regions(brain_regions, 4, [], True, False)
        edges = [(0, 1), (2, 3)] # edges from node 0 to 1 and node 2 to 3
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], self.color)
        edges = [(1, 2)]
        for edge in edges:
            self.add_edge([coords[edge[0]], coords[edge[1]]], [0.2, 0.8, 0.2, 1.0]) #specify any rgb color, last digit should be 1

    def set_clustering(self):
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
