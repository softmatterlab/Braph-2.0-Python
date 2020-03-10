import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
import pyqtgraph.Vector
import numpy as np

brain_distance_default = 230

class BrainWidget(GLViewWidget):
    def __init__(self, mesh_file, parent = None):
        super(BrainWidget, self).__init__(parent)
        self.brain_color = [0.7, 0.6, 0.55, 1]

    def init_brain_view(self, mesh_file):
        self.init_axis()
        self.init_grid()
        self.init_brain_mesh(mesh_file)

    def change_brain_mesh(self, mesh_file):
        self.removeItem(self.brain_mesh)
        self.init_brain_mesh(mesh_file)

    def init_brain_regions(self, brain_regions, visible):
        self.spheres = []
        self.brain_regions = brain_regions
        self.selected_regions = []

    def init_axis(self):
        self.ax = gl.GLAxisItem()
        self.ax.setSize(400,400,400)

    def init_grid(self):
        size = 250
        spacing = size/20
        self.grid = {}
        for ax in ['x', 'y', 'z']:
            self.grid[ax] = gl.GLGridItem()
            self.grid[ax].setSize(size,size,size)
            self.grid[ax].setSpacing(spacing,spacing,spacing)
        self.grid['x'].rotate(90, 0, 1, 0)
        self.grid['x'].translate(-size/2, 0, size/4)
        self.grid['y'].rotate(90, 1, 0, 0)
        self.grid['y'].translate(0, -size/2, size/4)
        self.grid['z'].translate(0, 0, -size/4)

    def init_brain_mesh(self, mesh_file):
        self.opts['distance'] = brain_distance_default
        self.setCameraPosition(azimuth=0)
        self.setBackgroundColor((200, 200, 200, 255))

        data = load_nv(mesh_file)
        self.brain_mesh = gl.GLMeshItem(vertexes=data['vertices'], faces=data['faces'], shader = 'normalColor')
        self.brain_mesh.setGLOptions('translucent')
        self.addItem(self.brain_mesh)

    def paintGL(self, *args, **kwds):
        GLViewWidget.paintGL(self, *args, **kwds)
        self.qglColor(QColor("k"))
        if self.show_labels_bool:
            for region in self.brain_regions:
                self.renderText(region.x, region.y, region.z, region.label)

    def load_brain_mesh(self, data):
        self.brain_mesh.setMeshData(vertexes=data['vertices'], faces=data['faces'])

    def change_transparency(self, alpha):
        new_color = self.brain_color
        new_color[-1] = alpha
        self.brain_color = new_color
        self.brain_mesh.setColor(self.brain_color)

    def show_3D(self):
        pass

    def sagittal_right(self):
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=0)

    def sagittal_left(self):
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=180)

    def axial_dorsal(self):
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance=brain_distance_default, elevation=90, azimuth=90)

    def axial_ventral(self):
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance=brain_distance_default, elevation=-90, azimuth=-90)

    def coronal_anterior(self):
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=90)

    def coronal_posterior(self):
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=-90)

    def show_brain(self, state):
        if state == 0:
            self.removeItem(self.brain_mesh)
        else:
            self.addItem(self.brain_mesh)

    def show_axis(self, state):
        if state == 0:
            self.removeItem(self.ax)
        else:
            self.addItem(self.ax)

    def show_grid(self, state):
        if state == 0:
            for grid in self.grid.values():
                self.removeItem(grid)
        else:
            for grid in self.grid.values():
                self.addItem(grid)

    def show_brain_regions(self, visible):
        if visible == 0:
            for sphere in self.spheres:
                self.removeItem(sphere)
        else:
            self.removeItem(self.brain_mesh)
            for sphere in self.spheres:
                self.addItem(sphere)
            self.addItem(self.brain_mesh)

    def show_labels(self, state):
        self.show_labels_bool = (state != 0)
        self.update()

    def select_region(self, index):
        self.selected_regions.append(index)
        self.spheres[index].setColor(self.sphere_color(index))

    def deselect_region(self, index):
        self.selected_regions.remove(index)
        self.spheres[index].setColor(self.sphere_color(index))

    def sphere_color(self, index):
        sphere_color = [.3, .3, 1.0, 1.0]
        if index in self.selected_regions:
            sphere_color = [1.0, .0, 2.0/3, 1.0]
        return sphere_color

    def generate_figure(self):
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "Image (*.png)")
        if file_name:
            fb = self.grabFrameBuffer()
            fb.save(file_name)

    def update_brain_regions(self):
        self.removeItem(self.brain_mesh)
        for sphere in self.spheres:
            try:
                self.removeItem(sphere)
            except:
                pass
        self.spheres = []
        for i in range(len(self.brain_regions)):
            brain_region = self.brain_regions[i]
            sphere_meshdata = gl.MeshData.sphere(8, 8, radius=4.0)
            sphere = gl.GLMeshItem(meshdata=sphere_meshdata, color = self.sphere_color(i), shader='shaded')
            sphere.translate(brain_region.x, brain_region.y, brain_region.z)
            sphere.setGLOptions('translucent')
            self.spheres.append(sphere)
            self.addItem(sphere)
        self.addItem(self.brain_mesh)

