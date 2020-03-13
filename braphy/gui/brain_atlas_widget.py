import pyqtgraph.opengl as gl
from PyQt5 import QtCore
from pyqtgraph.opengl import GLViewWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
import pyqtgraph.Vector
import numpy as np

brain_distance_default = 230

class BrainAtlasWidget(GLViewWidget):
    MOUSE_MODE_DEFAULT = 0
    MOUSE_MODE_ZOOM_IN = 1
    MOUSE_MODE_ZOOM_OUT = 2
    MOUSE_MODE_PAN = 3
    MOUSE_MODE_ROTATE = 4
    def __init__(self, mesh_file, parent = None):
        super(BrainAtlasWidget, self).__init__(parent)
        self.brain_color = [0.7, 0.6, 0.55, 1]
        self.mouse_mode = BrainAtlasWidget.MOUSE_MODE_DEFAULT
        self.gui_brain_regions = []
        self.show_labels_bool = 0
        self.init_axis()
        self.init_grid()

    def init_brain_view(self, mesh_file):
        self.init_brain_mesh(mesh_file)

    def change_brain_mesh(self, mesh_file):
        self.removeItem(self.brain_mesh)
        self.init_brain_mesh(mesh_file)

    def init_brain_regions(self, brain_regions, size, selected, show_brain_regions, show_only_selected):
        self.brain_regions = brain_regions
        self.brain_region_size = size
        self.show_brain_regions = show_brain_regions
        self.show_only_selected = show_only_selected
        self.update_brain_regions(selected)

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
            for gui_brain_region in self.gui_brain_regions:
                if self.brain_region_visible(gui_brain_region.selected):
                    pos = gui_brain_region.pos()
                    self.renderText(pos[0], pos[1], pos[2], gui_brain_region.label)

    def load_brain_mesh(self, data):
        self.brain_mesh.setMeshData(vertexes=data['vertices'], faces=data['faces'])

    def change_transparency(self, alpha):
        new_color = self.brain_color
        new_color[-1] = alpha
        self.brain_color = new_color
        self.brain_mesh.setColor(self.brain_color)

    def change_brain_region_size(self, size):
        for gui_brain_region in self.gui_brain_regions:
            gui_brain_region.set_size(size)

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

    def set_brain_regions_visible(self, visible):
        self.show_brain_regions = visible
        self.update_brain_regions_plot()

    def show_labels(self, state):
        self.show_labels_bool = (state != 0)
        self.update()

    def set_selected(self, selected):
        for index in range(len(self.gui_brain_regions)):
            if index in selected:
                self.select_region(index)
            else:
                self.deselect_region(index)

    def select_region(self, index):
        self.gui_brain_regions[index].set_selected(True)
        self.update_brain_regions_plot()

    def deselect_region(self, index):
        self.gui_brain_regions[index].set_selected(False)
        self.update_brain_regions_plot()

    def generate_figure(self):
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "Image (*.png)")
        if file_name:
            fb = self.grabFrameBuffer()
            fb.save(file_name)

    def brain_region_visible(self, selected):
        if selected:
            return self.show_brain_regions
        else:
            return ((not self.show_only_selected) and self.show_brain_regions)

    def update_brain_regions_plot(self):
        brain_removed = False
        try:
            self.removeItem(self.brain_mesh)
            brain_removed = True
        except:
            pass
        self.clear_gui_brain_regions()
        for gui_brain_region in self.gui_brain_regions:
            b = gui_brain_region.pos
            if self.brain_region_visible(gui_brain_region.selected):
                self.addItem(gui_brain_region)
        if brain_removed:
            self.addItem(self.brain_mesh)

    def update_brain_regions(self, selected_regions):
        self.gui_brain_regions = []
        for i in range(len(self.brain_regions)):
            selected = (i in selected_regions)
            brain_region = self.brain_regions[i]
            gui_brain_region = GUIBrainRegion(brain_region, self.brain_region_size, selected)
            gui_brain_region.add_observer(self.update)
            self.gui_brain_regions.append(gui_brain_region)
        self.update_brain_regions_plot()

    def mouseMoveEvent(self, ev):
        if ev.buttons() == QtCore.Qt.MidButton:
            diff = ev.pos() - self.mousePos
            self.mousePos = ev.pos()
            if (ev.modifiers() & QtCore.Qt.ControlModifier):
                self.pan(diff.x(), 0, diff.y(), relative=True)
            else:
                self.pan(diff.x(), diff.y(), 0, relative=True)
        if self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_DEFAULT:
            self.mouseMoveEventDefault(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ZOOM_IN:
            pass
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT:
            pass
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_PAN:
            self.mouseMoveEventPan(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ROTATE:
            self.mouseMoveEventRotate(ev)

    def mouseReleaseEvent(self, ev):
        if self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ZOOM_IN:
            self.mouseReleaseEventZoomIn(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT:
            self.mouseReleaseEventZoomOut(ev)

    def mouseMoveEventDefault(self, ev):
        diff = ev.pos() - self.mousePos
        self.mousePos = ev.pos()

        if ev.buttons() == QtCore.Qt.LeftButton:
            self.orbit(-diff.x(), diff.y())

    def mouseReleaseEventZoom(self, ev, delta):
        _, _, w, h = self.getViewport()
        dx = w/2-ev.pos().x()
        dy = h/2-ev.pos().y()
        self.pan(dx, 0, dy, relative=True)
        self.opts['distance'] *= 0.999**delta
        self.update()

    def mouseReleaseEventZoomIn(self, ev):
        self.mouseReleaseEventZoom(ev, 100)

    def mouseReleaseEventZoomOut(self, ev):
        self.mouseReleaseEventZoom(ev, -500)

    def mouseMoveEventPan(self, ev):
        diff = ev.pos() - self.mousePos
        self.mousePos = ev.pos()

        if ev.buttons() == QtCore.Qt.LeftButton:
            if (ev.modifiers() & QtCore.Qt.ControlModifier):
                self.pan(diff.x(), 0, diff.y(), relative=True)
            else:
                self.pan(diff.x(), diff.y(), 0, relative=True)

    def mouseMoveEventRotate(self, ev):
        diff = ev.pos() - self.mousePos
        self.mousePos = ev.pos()

        if ev.buttons() == QtCore.Qt.LeftButton:
            self.orbit(-diff.x(), diff.y())

    def get_gui_brain_region_items(self):
        gui_brain_region_items = []
        for item in self.items:
            if isinstance(item, GUIBrainRegion):
                gui_brain_region_items.append(item)
        return gui_brain_region_items

    def clear_gui_brain_regions(self):
        for item in self.get_gui_brain_region_items():
            self.removeItem(item)

class GUIBrainRegion(gl.GLMeshItem):
    def __init__(self, brain_region, size, selected):
        self.brain_region = brain_region
        self.label = self.brain_region.label
        self.x = self.brain_region.x
        self.y = self.brain_region.y
        self.z = self.brain_region.z
        meshdata = gl.MeshData.sphere(8, 8, radius=size)
        super().__init__(meshdata=meshdata, shader='shaded')
        self.set_selected(selected)
        self.translate(self.x, self.y, self.z)
        brain_region.add_observer(self.brain_region_changed)
        self.observers = []

    def brain_region_changed(self):
        self.label = self.brain_region.label
        self.update_pos()
        self.notify_observers()

    def update_pos(self):
        dx = self.brain_region.x - self.x
        dy = self.brain_region.y - self.y
        dz = self.brain_region.z - self.z
        self.x += dx
        self.y += dy
        self.z += dz
        self.translate(dx, dy, dz)

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer()

    def pos(self):
        return (self.x ,self.y, self.z)

    def set_selected(self, selected):
        self.selected = selected
        COLOR_PINK = [1.0, 0.0, 2.0/3, 1.0]
        COLOR_BLUE = [0.3, 0.3, 1.0, 1.0]
        color = COLOR_PINK if selected else COLOR_BLUE
        self.setColor(color)

    def set_size(self, size):
        meshdata = gl.MeshData.sphere(8, 8, radius=size)
        self.setMeshData(meshdata=meshdata)
