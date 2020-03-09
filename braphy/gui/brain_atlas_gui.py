import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/brain_atlas.ui")
brain_mesh_file = abs_path_from_relative(__file__, "BrainMesh_ICBM152.nv")
brain_distance_default = 230

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BrainAtlasGui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, atlas = None): # should be able to input atlas
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        if atlas == None:
            self.atlas = BrainAtlas()
        else:
            self.atlas = atlas
        self.setupUi(self)
        self.init_slider()
        self.init_buttons()
        self.init_actions()
        self.init_check_boxes()
        self.init_brain_view()
        self.check_boxes = []
        self.tableWidget.cellChanged.connect(self.changeCell)
        self.textEdit.setText(self.atlas.name)

    def init_slider(self):
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.valueChanged.connect(self.changeTransparency)

    def init_brain_view(self):
        self.init_axis()
        self.init_grid()
        self.init_brain_mesh()

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

    def init_brain_mesh(self):
        self.brain_color = [0.7, 0.6, 0.55, self.horizontalSlider.value()]
        self.graphicsView.opts['distance'] = brain_distance_default
        self.graphicsView.setCameraPosition(azimuth=0)
        self.graphicsView.setBackgroundColor((200, 200, 200, 255))
        data = load_nv(brain_mesh_file)
        colors = np.array([self.brain_color for i in range(len(data['faces']))])
        self.brain_mesh = gl.GLMeshItem(vertexes=data['vertices'], faces=data['faces'], shader = 'normalColor')
        self.brain_mesh.setGLOptions('translucent')
        self.graphicsView.addItem(self.brain_mesh)
        self.changeTransparency()

    def init_buttons(self):
       self.btnSelectAll.clicked.connect(self.select_all)
       self.btnClearSelection.clicked.connect(self.clear_selection)
       self.btnAdd.clicked.connect(self.add)
       self.btnAddAbove.clicked.connect(self.add_above)
       self.btnAddBelow.clicked.connect(self.add_below)
       self.btnRemove.clicked.connect(self.remove)
       self.btnMoveUp.clicked.connect(self.move_up)
       self.btnMoveDown.clicked.connect(self.move_down)
       self.btnMoveToTop.clicked.connect(self.move_to_top)
       self.btnMoveToBottom.clicked.connect(self.move_to_bottom)

       self.btn3D.clicked.connect(self.show_3D)
       self.btnSagittalLeft.clicked.connect(self.sagittal_left)
       self.btnSagittalRight.clicked.connect(self.sagittal_right)
       self.btnAxialDorsal.clicked.connect(self.axial_dorsal)
       self.btnAxialVentral.clicked.connect(self.axial_ventral)
       self.btnCoronalAnterior.clicked.connect(self.coronal_anterior)
       self.btnCoronalPosterior.clicked.connect(self.coronal_posterior)

    def init_actions(self):
        # TOOL BAR:
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.open)

        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPan.triggered.connect(self.pan)
        self.actionRotate.triggered.connect(self.rotate)
        self.actionFind.triggered.connect(self.find)

        group = QtWidgets.QActionGroup(self, exclusive = True)
        for action in (self.actionZoom_in, self.actionZoom_out, self.actionPan,
                       self.actionRotate, self.actionFind):
            group.addAction(action)

        self.actionSagittal_left.triggered.connect(self.sagittal_left)
        self.actionSagittal_right.triggered.connect(self.sagittal_right)
        self.actionAxial_dorsal.triggered.connect(self.axial_dorsal)
        self.actionAxial_ventral.triggered.connect(self.axial_ventral)
        self.actionCoronal_anterior.triggered.connect(self.coronal_anterior)
        self.actionCoronal_posterior.triggered.connect(self.coronal_posterior)

        self.actionView_brain.triggered.connect(self.show_brain)
        self.actionView_brain.setChecked(True)
        self.actionShow_axis.triggered.connect(self.show_axis)
        self.actionShow_grid.triggered.connect(self.show_grid)
        self.actionShow_brain_regions.triggered.connect(self.show_brain_regions)
        self.actionShow_labels.triggered.connect(self.show_labels)

        # MENU BAR:
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionImport_txt.triggered.connect(self.import_txt)
        self.actionImport_xls.triggered.connect(self.import_xls)
        self.actionImport_xml.triggered.connect(self.import_xml)
        self.actionExport_xml.triggered.connect(self.export_xml)
        self.actionExport_txt.triggered.connect(self.export_txt)
        self.actionClose.triggered.connect(self.close)

        self.actionSelect_all.triggered.connect(self.select_all)
        self.actionClear_selection.triggered.connect(self.clear_selection)
        self.actionAdd.triggered.connect(self.add)
        self.actionAdd_above.triggered.connect(self.add_above)
        self.actionAdd_below.triggered.connect(self.add_below)
        self.actionRemove.triggered.connect(self.remove)
        self.actionMove_up.triggered.connect(self.remove)
        self.actionMove_up.triggered.connect(self.move_up)
        self.actionMove_down.triggered.connect(self.move_down)
        self.actionMove_to_top.triggered.connect(self.move_to_top)
        self.actionMove_to_bottom.triggered.connect(self.move_to_bottom)

        self.actionGenerate_figure.triggered.connect(self.generate_figure)
        self.actionNew_MRI_Cohort.triggered.connect(self.new_mri_cohort)
        self.actionNew_fMRI_Cohort.triggered.connect(self.new_fmri_cohort)
        self.actionNew_EEG_Cohort.triggered.connect(self.new_eeg_cohort)
        self.actionNew_PET_Cohort.triggered.connect(self.new_pet_cohort)

        self.actionAbout.triggered.connect(self.about)


    def init_check_boxes(self):
        self.checkBoxShowBrain.stateChanged.connect(self.show_brain)
        self.checkBoxShowAxis.stateChanged.connect(self.show_axis)
        self.checkBoxShowGrid.stateChanged.connect(self.show_grid)
        self.checkBoxShowBrainRegions.stateChanged.connect(self.show_brain_regions)
        self.checkBoxShowLabels.stateChanged.connect(self.show_labels)

    def show_brain(self, state):
        if (self.actionView_brain.isChecked() != self.checkBoxShowBrain.isChecked()):
            if state == 0: #not checked
                self.graphicsView.removeItem(self.brain_mesh)
                self.actionView_brain.setChecked(False)
                self.checkBoxShowBrain.setChecked(False)
            else: #checked
                self.graphicsView.addItem(self.brain_mesh)
                self.actionView_brain.setChecked(True)
                self.checkBoxShowBrain.setChecked(True)

    def show_axis(self, state):
        if (self.actionShow_axis.isChecked() != self.checkBoxShowAxis.isChecked()):
            if state == 0: #not checked
                self.graphicsView.removeItem(self.ax)
                self.actionShow_axis.setChecked(False)
                self.checkBoxShowAxis.setChecked(False)
            else: #checked
                self.graphicsView.addItem(self.ax)
                self.actionShow_axis.setChecked(True)
                self.checkBoxShowAxis.setChecked(True)

    def show_grid(self, state):
        if (self.actionShow_grid.isChecked() != self.checkBoxShowGrid.isChecked()):
            if state == 0:
                for grid in self.grid.values():
                    self.graphicsView.removeItem(grid)
                self.actionShow_grid.setChecked(False)
                self.checkBoxShowGrid.setChecked(False)
            else:
                for grid in self.grid.values():
                    self.graphicsView.addItem(grid)
                self.actionShow_grid.setChecked(True)
                self.checkBoxShowGrid.setChecked(True)

    def show_brain_regions(self, state):
        pass

    def show_labels(self, state):
        pass

    def select_all(self):
        selected = np.arange(len(self.atlas.brain_regions))
        self.set_checked(selected)

    def clear_selection(self):
        self.set_checked(np.array([]))

    def add(self):
        self.atlas.add_brain_region()
        self.update_table()

    def add_above(self):
        self.tableWidget.setEnabled(False)
        selected, added = self.atlas.add_above_brain_regions(self.get_checked())
        self.update_table(selected)

    def add_below(self):
        selected, added = self.atlas.add_below_brain_regions(self.get_checked())
        self.update_table(selected)

    def remove(self):
        selected = self.atlas.remove_brain_regions(self.get_checked())
        self.update_table(selected)

    def move_up(self):
        selected = self.atlas.move_up_brain_regions(self.get_checked())
        self.update_table(selected)

    def move_down(self):
        selected = self.atlas.move_down_brain_regions(self.get_checked())
        self.update_table(selected)

    def move_to_top(self):
        selected = self.atlas.move_to_top_brain_regions(self.get_checked())
        self.update_table(selected)

    def move_to_bottom(self):
        selected = self.atlas.move_to_bottom_brain_regions(self.get_checked())
        self.update_table(selected)

    def changeCell(self, row, column):
        if column == 1:
            self.atlas.brain_regions[row].label = self.tableWidget.item(row, column).text()
        elif column == 2:
            self.atlas.brain_regions[row].name = self.tableWidget.item(row, column).text()
        elif column == 3:
            self.atlas.brain_regions[row].x = float(self.tableWidget.item(row, column).text())
        elif column == 4:
            self.atlas.brain_regions[row].y = float(self.tableWidget.item(row, column).text())
        elif column == 5:
            self.atlas.brain_regions[row].z = float(self.tableWidget.item(row, column).text())
        elif column == 6:
            pass #left/right
        elif column == 7:
            pass #Notes

    def changeTransparency(self):
        alpha = self.horizontalSlider.value()/100.0
        new_color = self.brain_color
        new_color[-1] = alpha
        self.brain_color = new_color
        self.brain_mesh.setColor(self.brain_color)

    def update_table(self, selected = None):
        if np.any(selected == None):
            selected = self.get_checked()

        self.tableWidget.blockSignals(True)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.check_boxes = []

        for i in range(self.atlas.brain_region_number()):
            self.tableWidget.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)
            check_box = QCheckBox()
            self.check_boxes.append(check_box)
            if i in selected:
                self.check_boxes[i].setChecked(True)
            layout.addWidget(self.check_boxes[i])
            widget.setLayout(layout)
            self.tableWidget.setCellWidget(i, 0, widget)

            item = QTableWidgetItem(self.atlas.brain_regions[i].label)
            self.tableWidget.setItem(i, 1, item)

            item = QTableWidgetItem(self.atlas.brain_regions[i].name)
            self.tableWidget.setItem(i, 2, item)

            item = QTableWidgetItem(str(self.atlas.brain_regions[i].x))
            self.tableWidget.setItem(i, 3, item)

            item = QTableWidgetItem(str(self.atlas.brain_regions[i].y))
            self.tableWidget.setItem(i, 4, item)

            item = QTableWidgetItem(str(self.atlas.brain_regions[i].z))
            self.tableWidget.setItem(i, 5, item)

        self.tableWidget.blockSignals(False)

    def set_checked(self, selected):
        for i in range(len(self.check_boxes)):
            if i in selected:
                self.check_boxes[i].setChecked(True)
            else:
                self.check_boxes[i].setChecked(False)

    def get_checked(self):
        selected = []
        for i in range(len(self.check_boxes)):
            if self.check_boxes[i].isChecked():
                selected.append(i)
        return np.array(selected)

    def save(self):
        pass

    def open(self):
        pass

    def zoom_in(self):
        self.graphicsView.setCursor(QtCore.Qt.ForbiddenCursor)

    def zoom_out(self):
        self.graphicsView.setCursor(QtCore.Qt.SizeHorCursor)

    def pan(self):
        self.graphicsView.setCursor(QtCore.Qt.OpenHandCursor)

    def rotate(self):
        self.graphicsView.setCursor(QtCore.Qt.ForbiddenCursor)

    def find(self):
        self.graphicsView.setCursor(QtCore.Qt.CrossCursor)

    def show_3D(self):
        pass

    def sagittal_right(self):
        self.graphicsView.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=0)

    def sagittal_left(self):
        self.graphicsView.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=180)

    def axial_dorsal(self):
        self.graphicsView.setCameraPosition(distance=brain_distance_default, elevation=90, azimuth=90)

    def axial_ventral(self):
        self.graphicsView.setCameraPosition(distance=brain_distance_default, elevation=-90, azimuth=-90)

    def coronal_anterior(self):
        self.graphicsView.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=90)

    def coronal_posterior(self):
        self.graphicsView.setCameraPosition(distance=brain_distance_default, elevation=0, azimuth=-90)

    def save_as(self):
        pass

    def import_txt(self):
        pass

    def import_xls(self):
        pass

    def import_xml(self):
        pass

    def export_xml(self):
        pass

    def export_txt(self):
        pass

    def close(self):
        pass

    def generate_figure(self):
        pass

    def new_mri_cohort(self):
        pass

    def new_fmri_cohort(self):
        pass

    def new_eeg_cohort(self):
        pass

    def new_pet_cohort(self):
        pass

    def about(self):
        pass

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = BrainAtlasGui()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
