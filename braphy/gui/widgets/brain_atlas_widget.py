import pyqtgraph.opengl as gl
from PyQt5 import QtCore, uic, QtWidgets
from pyqtgraph.opengl import GLViewWidget
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.gui_brain_region import GUIBrainRegion
from braphy.gui.gui_brain_edge import GUIBrainEdge
import pyqtgraph.Vector
import numpy as np

ui_file = abs_path_from_relative(__file__, "../ui_files/brain_atlas_widget.ui")
Form, Base = uic.loadUiType(ui_file)

brain_distance_default = 235

class BrainAtlasWidget(GLViewWidget):
    MOUSE_MODE_DEFAULT = 0
    MOUSE_MODE_ZOOM_IN = 1
    MOUSE_MODE_ZOOM_OUT = 2
    MOUSE_MODE_PAN_Y = 3
    MOUSE_MODE_PAN_Z = 4
    MOUSE_MODE_ROTATE = 5
    MOUSE_MODE_FIND = 6
    def __init__(self, parent = None):
        super(BrainAtlasWidget, self).__init__(parent)
        self.brain_color = [0.7, 0.6, 0.55, 1]
        self.mouse_mode = BrainAtlasWidget.MOUSE_MODE_DEFAULT
        self.gui_brain_regions = []
        self.show_labels_bool = 0
        self.orthographic = False
        self.init_axis()
        self.init_grid()
        self.interaction_enabled = True
        self.selection_enabled = True
        self.timer = None
        self.brain_mesh = None
        self.brainBackgroundColor = (200, 200, 200, 255)
        self.selected_observers = []
        self.region_color = [0.3, 0.3, 1.0, 1.0] # blue
        self.selected_region_color = [1.0, 0.0, 2.0/3, 1.0] # pink
        self.tool_bar = BrainAtlasWidgetToolBar(self)

    def width(self):
        return super().width() * self.devicePixelRatio()

    def height(self):
        return super().height() * self.devicePixelRatio()

    def add_selected_observer(self, observer):
        self.selected_observers.append(observer)

    def setBrainBackgroundColor(self, rgba):
        self.brainBackgroundColor = rgba
        self.setBackgroundColor(self.brainBackgroundColor)

    def get_actions(self):
        return self.tool_bar.get_actions()

    def update_orbit(self):
        self.orbit(0.5, 0)

    def set_locked(self, locked):
        if locked:
            self.interaction_enabled = False
        else:
            self.interaction_enabled = True

    def animate(self, on):
        if not self.timer:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_orbit)
        self.set_locked(on)
        if on:
            self.timer.start(10)
        else:
            self.timer.stop()

    def set_orthographic(self, orthographic):
        if orthographic:
            self.orthographic = True
            self.opts['fov'] = 0.1
            self.setCameraPosition(distance = 160000)
        else:
            self.orthographic = False
            self.opts['fov'] = 60
            self.setCameraPosition(distance = brain_distance_default)

    def set_brain_mesh(self, mesh_data):
        if self.brain_mesh in self.items:
            self.removeItem(self.brain_mesh)
        self.init_brain_mesh(mesh_data)

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

    def init_brain_mesh(self, mesh_data):
        self.opts['distance'] = brain_distance_default
        self.setBackgroundColor(self.brainBackgroundColor)

        self.brain_mesh = gl.GLMeshItem(vertexes=mesh_data['vertices'], faces=mesh_data['faces'], shader = 'normalColor')
        self.brain_mesh.setGLOptions('translucent')
        self.addItem(self.brain_mesh)

    def set_shader(self, shader):
        self.brain_mesh.setShader(shader)

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

    def reset_brain_region_colors(self):
        self.set_brain_region_color(self.region_color)
        self.set_selected_brain_region_color(self.selected_region_color)

    def set_brain_region_color(self, color):
        self.region_color = color
        for gui_brain_region in self.gui_brain_regions:
            gui_brain_region.color = color
            if not gui_brain_region.selected:
                gui_brain_region.setColor(color)

    def set_selected_brain_region_color(self, color):
        self.selected_region_color = color
        for gui_brain_region in self.gui_brain_regions:
            gui_brain_region.selected_color = color
            if gui_brain_region.selected:
                gui_brain_region.setColor(color)

    def show_3D(self):
        self.set_orthographic(False)
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(distance = brain_distance_default, elevation = 30, azimuth = 45)

    def fixed_view(self, elevation, a):
        self.set_orthographic(True)
        self.opts['center'] = pyqtgraph.Vector(0, 0, 0)
        self.setCameraPosition(elevation=elevation, a=azimuth)

    def sagittal_right(self):
        self.fixed_view(0, 0)

    def sagittal_left(self):
        self.fixed_view(0, 180)

    def axial_dorsal(self):
        self.fixed_view(90, 90)

    def axial_ventral(self):
        self.fixed_view(-90, -90)

    def coronal_anterior(self):
        self.fixed_view(0, 90)

    def coronal_posterior(self):
        self.fixed_view(0, -90)

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

    def deselect_all(self):
        for region in self.gui_brain_regions:
            region.set_selected(False)
        self.update_brain_regions_plot()

    def generate_figure(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "Save figure", "untitled.png",
                                                      "Image (*.png)", options = options)
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
            gui_brain_region = GUIBrainRegion(brain_region, self.brain_region_size, selected, self.region_color, self.selected_region_color)
            gui_brain_region.add_observer(self.update)
            gui_brain_region.add_selected_observer(self.selected_updated)
            self.gui_brain_regions.append(gui_brain_region)
        self.update_brain_regions_plot()

    def selected_updated(self):
        selected = []
        for i, gui_brain_region in enumerate(self.gui_brain_regions):
            if gui_brain_region.selected:
                selected.append(i)
        for observer in self.selected_observers:
            observer(selected)

    def wheelEvent(self, ev):
        if not self.interaction_enabled:
            return
        super().wheelEvent(ev)

    def mouseMoveEvent(self, ev):
        if not self.interaction_enabled:
            return
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
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_PAN_Y:
            self.mouseMoveEventPan(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_PAN_Z:
            self.mouseMoveEventPan(ev, invert=True)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ROTATE:
            self.mouseMoveEventRotate(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_FIND:
            pass

    def gui_brain_region_at(self, click_pos_2D, camera_pos):
        closest_region = None
        closest_region_distance = np.inf
        m = self.projectionMatrix() * self.viewMatrix()
        for gui_brain_region in self.gui_brain_regions:
            pos = gui_brain_region.pos()
            pos = QtGui.QVector3D(pos[0], pos[1], pos[2])
            orthogonal_direction = QtGui.QVector3D(0, pos.z() - camera_pos.z(), camera_pos.y() - pos.y())
            orthonormal_direction = orthogonal_direction.normalized()
            sphere_surface_pos = pos + gui_brain_region.size * orthonormal_direction

            pos_2D = m.map(pos)
            sphere_surface_pos_2D = m.map(sphere_surface_pos)
            sphere_radius_2D = pos_2D.distanceToPoint(sphere_surface_pos_2D)

            dist_to_click = pow(pow(click_pos_2D[0]-pos_2D[0], 2) + pow(click_pos_2D[1]-pos_2D[1], 2), 0.5)
            camera_distance = pos.distanceToPoint(camera_pos)

            if dist_to_click < sphere_radius_2D:
                if camera_distance < closest_region_distance:
                    closest_region_distance = camera_distance
                    closest_region = gui_brain_region
        return closest_region

    def enable_brain_region_selection(self, enable):
        self.selection_enabled = enable
        self.tool_bar.actionFind.setEnabled(enable)

    def mouseReleaseEvent(self, ev):
        if not self.interaction_enabled:
            return
        if self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ZOOM_IN:
            self.mouseReleaseEventZoomIn(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT:
            self.mouseReleaseEventZoomOut(ev)
        elif self.mouse_mode == BrainAtlasWidget.MOUSE_MODE_FIND:
            self.mouseReleaseEventFind(ev)
            return
        self.mouseReleaseEventDefault(ev)

    def mouseReleaseEventDefault(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.mouseReleaseEventFind(ev)

    def mouseMoveEventDefault(self, ev):
        if ev.buttons() == QtCore.Qt.LeftButton:
            diff = ev.pos() - self.mousePos
            self.mousePos = ev.pos()
            if self.orthographic:
                self.set_orthographic(False)
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

    def mouseReleaseEventFind(self, ev):
        if not self.selection_enabled:
            return
        mouse_travel_distance = (ev.pos() - self.mousePos).manhattanLength()
        if mouse_travel_distance > 15:
            return
        x = (ev.pos().x()-super().width()/2)/(super().width()/2)
        y = -(ev.pos().y()-super().height()/2)/(super().height()/2)
        m = self.projectionMatrix() * self.viewMatrix()
        camera_pos = m.inverted()[0].map(QtGui.QVector3D(0,0,0))
        closest_region = self.gui_brain_region_at([x,y], camera_pos)
        if closest_region:
            closest_region.toggle_selected()
            if closest_region.selected:
                tool_tip_label = "{}\n{}\n{}".format(closest_region.label, closest_region.brain_region.name, closest_region.pos())
                QtGui.QToolTip.showText(self.mapToGlobal(ev.pos()), tool_tip_label, self)

    def mouseMoveEventPan(self, ev, invert = False):
        diff = ev.pos() - self.mousePos
        self.mousePos = ev.pos()

        if ev.buttons() == QtCore.Qt.LeftButton:
            pan_z = bool(ev.modifiers() & QtCore.Qt.ControlModifier) ^ invert
            if pan_z:
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

    def get_gui_brain_edge_items(self):
        gui_brain_edge_items = []
        for item in self.items:
            if isinstance(item, GUIBrainEdge):
                gui_brain_edge_items.append(item)
        return gui_brain_edge_items

    def clear_gui_brain_regions(self):
        for item in self.get_gui_brain_region_items():
            self.removeItem(item)

    def clear_gui_brain_edges(self):
        for item in self.get_gui_brain_edge_items():
            self.removeItem(item)

    def set_cursor(self, file_name):
        cursor_file = abs_path_from_relative(__file__, file_name)
        pm = QtGui.QPixmap(cursor_file)
        cursor = QtGui.QCursor(pm)
        self.setCursor(cursor)

    def zoom_in(self):
        self.check_cursor(BrainAtlasWidget.MOUSE_MODE_ZOOM_IN, '../icons/zoom_in.png')

    def zoom_out(self):
        self.check_cursor(BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT, '../icons/zoom_out.png')

    def pan_y(self):
        self.check_cursor(BrainAtlasWidget.MOUSE_MODE_PAN_Y, '../icons/hand_xy.png')

    def pan_z(self):
        self.check_cursor(BrainAtlasWidget.MOUSE_MODE_PAN_Z, '../icons/hand_xz.png')

    def rotate(self):
        self.check_cursor(BrainAtlasWidget.MOUSE_MODE_ROTATE, '../icons/rotate.png')

    def find(self):
        self.check_cursor(BrainAtlasWidget.MOUSE_MODE_FIND, '../icons/cursor.png')

    def check_cursor(self, mode, icon):
        if self.mouse_mode == mode:
            self.mouse_mode = BrainAtlasWidget.MOUSE_MODE_DEFAULT
            self.unsetCursor()
            self.tool_bar.actionDefault.trigger()
        else:
            self.mouse_mode = mode
            self.set_cursor(icon)

    def add_edge(self, coords, color):
        brain_removed = False
        try:
            self.removeItem(self.brain_mesh)
            brain_removed = True
        except:
            pass
        brain_edge = GUIBrainEdge(color, coords[0], coords[1])
        self.addItem(brain_edge)
        if brain_removed:
            self.addItem(self.brain_mesh)

class BrainAtlasWidgetToolBar(Base, Form):
    def __init__(self, brain_atlas_widget, parent = None):
        super(BrainAtlasWidgetToolBar, self).__init__(parent)
        self.setupUi(self)
        self.brain_atlas_widget = brain_atlas_widget
        self.init_actions()

    def init_actions(self):
        group = QtWidgets.QActionGroup(self)
        for action in self.get_actions():
            group.addAction(action)
        self.actionDefault = QtWidgets.QAction()
        self.actionDefault.setCheckable(True)
        group.addAction(self.actionDefault)
        self.actionZoom_in.triggered.connect(self.brain_atlas_widget.zoom_in)
        self.actionZoom_out.triggered.connect(self.brain_atlas_widget.zoom_out)
        self.actionPan_x_y.triggered.connect(self.brain_atlas_widget.pan_y)
        self.actionPan_z.triggered.connect(self.brain_atlas_widget.pan_z)
        self.actionRotate.triggered.connect(self.brain_atlas_widget.rotate)
        self.actionFind.triggered.connect(self.brain_atlas_widget.find)

    def get_actions(self):
        actions = [self.actionZoom_in, self.actionZoom_out, self.actionPan_x_y, self.actionPan_z,
                   self.actionRotate, self.actionFind]
        return actions
