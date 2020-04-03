import sys
import os
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.utility.helper_functions import abs_path_from_relative, load_nv, get_version_info
import numpy as np
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/brain_atlas.ui")
brain_mesh_file_name_default = "meshes/BrainMesh_ICBM152.nv"
brain_mesh_file_default = abs_path_from_relative(__file__, brain_mesh_file_name_default)

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BrainAtlasGui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None, atlas = None): # should be able to input atlas
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.locked = False
        if atlas:
            self.atlas = atlas
        else:
            self.atlas = BrainAtlas(mesh_file = brain_mesh_file_name_default.split('/')[-1])
        self.init_check_boxes()
        self.init_brain_widget(brain_mesh_file_default)
        self.init_buttons()
        self.init_actions()

        self.init_combo_box()
        self.init_sliders()
        self.tableWidget.cellChanged.connect(self.change_cell)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.itemSelectionChanged.connect(self.region_selection_changed)

        self.textAtlasName.setText(self.atlas.name)
        self.meshName.setText('Brain View')
        self.textAtlasName.textChanged.connect(self.atlas_name_change)
        self.file_name = None
        self.loaded_mesh_data = None

        self.brainWidget.add_selected_observer(self.set_selected)

    def to_file(self, atlas_file):
        with open(atlas_file, 'w') as f:
            json.dump(self.to_dict(), f, sort_keys=True, indent=4)

    def to_dict(self):
        d = {}
        brain_mesh_data = {}
        brain_mesh_data['vertices'] = self.brain_mesh_data['vertices'].tolist()
        brain_mesh_data['faces'] = self.brain_mesh_data['faces'].tolist()
        d['brain_mesh_data'] = brain_mesh_data
        d['version'] = get_version_info()
        d['atlas'] = self.atlas.to_dict()
        return d

    def from_file(self, atlas_file):
        with open(atlas_file, 'r') as f:
            d = json.load(f)
        self.from_dict(d)
        self.file_name = atlas_file

    def from_dict(self, d):
        self.atlas = BrainAtlas.from_dict(d['atlas'])
        vertices = np.asarray(d['brain_mesh_data']['vertices'])
        faces = np.asarray(d['brain_mesh_data']['faces'])
        brain_mesh_data = {'vertices': vertices, 'faces': faces}
        self.brain_mesh_data = brain_mesh_data
        self.set_brain_mesh_data()
        self.set_brain_regions()
        self.atlas_name_change()
        self.add_mesh_to_combobox(self.atlas.mesh_file)
        self.loaded_mesh_data = (self.atlas.mesh_file, brain_mesh_data)
        self.update_table()

    def add_mesh_to_combobox(self, mesh_file_name):
        self.comboBox.blockSignals(True)
        idx = self.comboBox.findText(mesh_file_name)
        if idx > -1:
            self.comboBox.setCurrentIndex(idx)
        else:
            self.comboBox.insertItem(self.comboBox.count() - 2, mesh_file_name)
            self.comboBox.setCurrentText(mesh_file_name)
        self.comboBox.blockSignals(False)

    def set_brain_mesh_file(self, brain_mesh_file):
        self.brain_mesh_file_name = brain_mesh_file.split('/')[-1]
        self.atlas.mesh_file = self.brain_mesh_file_name
        self.brain_mesh_data = load_nv(brain_mesh_file)
        self.set_brain_mesh_data()

    def set_brain_mesh_data(self):
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.change_transparency()

    def set_brain_regions(self):
        size = self.sliderRegions.value()/10.0
        show_only_selected = self.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.atlas.brain_regions, size, self.get_selected(), show_brain_regions, show_only_selected)

    def init_brain_widget(self, brain_mesh_file):
        self.brain_mesh_file_name = brain_mesh_file.split('/')[-1]
        self.brain_mesh_data = load_nv(brain_mesh_file)
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.set_brain_regions()

    def init_combo_box(self):
        self.mesh_file_paths = []
        nv_files = self.get_all_nv_files()
        for file in nv_files:
            self.comboBox.addItem(file)
            self.mesh_file_paths.append(abs_path_from_relative(__file__, 'meshes/{}'.format(file)))

        self.comboBox.insertSeparator(self.comboBox.count())
        self.comboBox.addItem('Open...')
        idx = self.comboBox.findText(self.brain_mesh_file_name)
        self.comboBox.setCurrentIndex(idx)
        self.comboBox.currentIndexChanged.connect(self.select_brain_mesh)
        self.last_combobox_index = idx

    def set_locked(self, locked):
        self.locked = locked
        lock_items = [self.comboBox, self.textAtlasName, self.actionOpen, self.actionImport_file,
                      self.btnAdd, self.btnAddAbove, self.btnAddBelow, self.btnRemove,
                      self.actionAdd, self.actionAdd_above, self.actionAdd_below, self.actionRemove]
        for item in lock_items:
            item.setEnabled(not self.locked)

        self.tableWidget.blockSignals(True)
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                flags = (QtCore.Qt.ItemIsSelectable) if self.locked else (QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                item = self.tableWidget.item(row, col)
                if item:
                    item.setFlags(flags)
        self.tableWidget.blockSignals(False)

    def select_brain_mesh(self, i):
        if self.comboBox.currentText() == 'Open...':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","nv files (*.nv)", options=options)
            if file_path:
                file_name = file_path.split('/')[-1]
                self.comboBox.blockSignals(True)
                self.comboBox.insertItem(self.comboBox.count() - 2, file_name)
                self.comboBox.setCurrentText(file_name)
                self.comboBox.blockSignals(False)
                self.mesh_file_paths.append(file_path)
                self.last_combobox_index = self.comboBox.count() - 3
            else:
                self.comboBox.blockSignals(True)
                self.comboBox.setCurrentIndex(self.last_combobox_index)
                self.comboBox.blockSignals(False)
        else:
            if self.loaded_mesh_data:
                if i == self.comboBox.findText(self.loaded_mesh_data[0]):
                    self.brain_mesh_data = self.loaded_mesh_data[1]
                    self.set_brain_mesh_data()
                    return
            file_path = self.mesh_file_paths[i]
            self.last_combobox_index = i
        if file_path:
            self.set_brain_mesh_file(file_path)

    def get_all_nv_files(self):
        dir = abs_path_from_relative(__file__, 'meshes')
        nv_files = [f for f in os.listdir(dir) if f.endswith('.nv')]
        return nv_files

    def init_sliders(self):
        self.sliderBrain.valueChanged.connect(self.change_transparency)
        self.sliderBrain.setValue(50)
        self.sliderRegions.valueChanged.connect(self.change_brain_region_size)

    def change_transparency(self):
        alpha = self.sliderBrain.value()/100.0
        self.brainWidget.change_transparency(alpha)

    def change_brain_region_size(self):
        size = self.sliderRegions.value()/10.0
        self.brainWidget.change_brain_region_size(size)

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

        self.btn3D.clicked.connect(self.brainWidget.show_3D)
        self.btnSagittalLeft.clicked.connect(self.brainWidget.sagittal_left)
        self.btnSagittalRight.clicked.connect(self.brainWidget.sagittal_right)
        self.btnAxialDorsal.clicked.connect(self.brainWidget.axial_dorsal)
        self.btnAxialVentral.clicked.connect(self.brainWidget.axial_ventral)
        self.btnCoronalAnterior.clicked.connect(self.brainWidget.coronal_anterior)
        self.btnCoronalPosterior.clicked.connect(self.brainWidget.coronal_posterior)

    def init_actions(self):
        # TOOL BAR:
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.open)

        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPanY.triggered.connect(self.pan_y)
        self.actionPanZ.triggered.connect(self.pan_z)
        self.actionRotate.triggered.connect(self.rotate)
        self.actionFind.triggered.connect(self.find)

        group = QtWidgets.QActionGroup(self)
        for action in (self.actionZoom_in, self.actionZoom_out, self.actionPanY,
                       self.actionPanZ, self.actionRotate, self.actionFind):
            group.addAction(action)

        self.action3D.triggered.connect(self.brainWidget.show_3D)
        self.actionSagittal_left.triggered.connect(self.brainWidget.sagittal_left)
        self.actionSagittal_right.triggered.connect(self.brainWidget.sagittal_right)
        self.actionAxial_dorsal.triggered.connect(self.brainWidget.axial_dorsal)
        self.actionAxial_ventral.triggered.connect(self.brainWidget.axial_ventral)
        self.actionCoronal_anterior.triggered.connect(self.brainWidget.coronal_anterior)
        self.actionCoronal_posterior.triggered.connect(self.brainWidget.coronal_posterior)

        self.actionView_brain.triggered.connect(self.show_brain)
        self.actionView_brain.setChecked(True)
        self.actionShow_axis.triggered.connect(self.show_axis)
        self.actionShow_axis.setChecked(True)
        self.actionShow_grid.triggered.connect(self.show_grid)
        self.actionShow_grid.setChecked(True)
        self.actionShow_brain_regions.triggered.connect(self.show_brain_regions)
        self.actionShow_brain_regions.setChecked(True)
        self.actionShow_labels.triggered.connect(self.show_labels)
        self.actionShow_labels.setChecked(True)

        # MENU BAR:
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionImport_file.triggered.connect(self.import_file)
        self.actionExport_xml.triggered.connect(self.export_xml)
        self.actionExport_txt.triggered.connect(self.export_txt)
        self.actionClose.triggered.connect(self.close)

        self.actionSelect_all.triggered.connect(self.select_all)
        self.actionClear_selection.triggered.connect(self.clear_selection)
        self.actionAdd.triggered.connect(self.add)
        self.actionAdd_above.triggered.connect(self.add_above)
        self.actionAdd_below.triggered.connect(self.add_below)
        self.actionRemove.triggered.connect(self.remove)
        self.actionMove_up.triggered.connect(self.move_up)
        self.actionMove_down.triggered.connect(self.move_down)
        self.actionMove_to_top.triggered.connect(self.move_to_top)
        self.actionMove_to_bottom.triggered.connect(self.move_to_bottom)

        self.actionGenerate_figure.triggered.connect(self.brainWidget.generate_figure)
        self.actionBrainViewOpen.triggered.connect(self.brain_view_open)

        self.actionNew_MRI_Cohort.triggered.connect(self.new_mri_cohort)
        self.actionNew_fMRI_Cohort.triggered.connect(self.new_fmri_cohort)
        self.actionNew_EEG_Cohort.triggered.connect(self.new_eeg_cohort)
        self.actionNew_PET_Cohort.triggered.connect(self.new_pet_cohort)

        self.actionAbout.triggered.connect(self.about)

    def init_check_boxes(self):
        self.checkBoxShowBrainRegions.stateChanged.connect(self.show_brain_regions)
        self.checkBoxShowBrainRegions.setChecked(True)
        self.checkBoxShowBrain.stateChanged.connect(self.show_brain)
        self.checkBoxShowBrain.setChecked(True)
        self.checkBoxShowAxis.stateChanged.connect(self.show_axis)
        self.checkBoxShowAxis.setChecked(True)
        self.checkBoxShowGrid.stateChanged.connect(self.show_grid)
        self.checkBoxShowGrid.setChecked(True)
        self.checkBoxShowLabels.stateChanged.connect(self.show_labels)
        self.checkBoxShowLabels.setChecked(True)
        self.checkBoxShowOnlySelected.stateChanged.connect(self.show_only_selected)

    def show_brain(self, state):
        if (self.actionView_brain.isChecked() != self.checkBoxShowBrain.isChecked()):
            self.brainWidget.show_brain(state)
            self.actionView_brain.setChecked(state != 0)
            self.checkBoxShowBrain.setChecked(state != 0)

    def show_axis(self, state):
        if (self.actionShow_axis.isChecked() != self.checkBoxShowAxis.isChecked()):
            self.brainWidget.show_axis(state)
            self.actionShow_axis.setChecked(state != 0)
            self.checkBoxShowAxis.setChecked(state != 0)

    def show_grid(self, state):
        if (self.actionShow_grid.isChecked() != self.checkBoxShowGrid.isChecked()):
            self.brainWidget.show_grid(state)
            self.actionShow_grid.setChecked(state != 0)
            self.checkBoxShowGrid.setChecked(state != 0)

    def show_brain_regions(self, state):
        if (self.actionShow_brain_regions.isChecked() != self.checkBoxShowBrainRegions.isChecked()):
            self.brainWidget.set_brain_regions_visible(state != 0)
            self.actionShow_brain_regions.setChecked(state != 0)
            self.checkBoxShowBrainRegions.setChecked(state != 0)
            if state == 0:
                self.checkBoxShowLabels.setChecked(False)
                self.checkBoxShowLabels.setEnabled(False)
                self.checkBoxShowOnlySelected.setChecked(False)
                self.checkBoxShowOnlySelected.setEnabled(False)
            else:
                self.checkBoxShowLabels.setEnabled(True)
                self.checkBoxShowOnlySelected.setEnabled(True)

    def show_labels(self, state):
        if (self.actionShow_labels.isChecked() != self.checkBoxShowLabels.isChecked()):
            self.brainWidget.show_labels(state)
            self.actionShow_labels.setChecked(state != 0)
            self.checkBoxShowLabels.setChecked(state != 0)

    def show_only_selected(self, state):
        self.brainWidget.show_only_selected = (state != 0)
        self.brainWidget.update_brain_regions_plot()

    def select_all(self):
        self.tableWidget.selectAll()

    def clear_selection(self):
        self.tableWidget.clearSelection()

    def add(self):
        self.atlas.add_brain_region()
        self.update_table()

    def add_above(self):
        selected, added = self.atlas.add_above_brain_regions(self.get_selected())
        self.update_table(selected)

    def add_below(self):
        selected, added = self.atlas.add_below_brain_regions(self.get_selected())
        self.update_table(selected)

    def remove(self):
        selected = self.atlas.remove_brain_regions(self.get_selected())
        self.update_table(selected)

    def move_up(self):
        selected = self.atlas.move_up_brain_regions(self.get_selected())
        self.update_table(selected)

    def move_down(self):
        selected = self.atlas.move_down_brain_regions(self.get_selected())
        self.update_table(selected)

    def move_to_top(self):
        selected = self.atlas.move_to_top_brain_regions(self.get_selected())
        self.update_table(selected)

    def move_to_bottom(self):
        selected = self.atlas.move_to_bottom_brain_regions(self.get_selected())
        self.update_table(selected)

    def atlas_name_change(self):
        self.atlas.name = self.textAtlasName.toPlainText()

    def change_cell(self, row, column):
        if column == 0:
            self.atlas.brain_regions[row].set(label = self.tableWidget.item(row, column).text())
        elif column == 1:
            self.atlas.brain_regions[row].set(name = self.tableWidget.item(row, column).text())
        elif column == 2:
            self.atlas.brain_regions[row].set(x = float(self.tableWidget.item(row, column).text()))
        elif column == 3:
            self.atlas.brain_regions[row].set(y = float(self.tableWidget.item(row, column).text()))
        elif column == 4:
            self.atlas.brain_regions[row].set(z = float(self.tableWidget.item(row, column).text()))
        elif column == 5:
            pass #left/right
        elif column == 6:
            pass #Notes

    def update_table(self, selected = None):
        if np.any(selected == None):
            selected = self.get_selected()

        self.tableWidget.blockSignals(True)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for i in range(self.atlas.brain_region_number()):
            self.tableWidget.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)

            item = QTableWidgetItem(self.atlas.brain_regions[i].label)
            self.tableWidget.setItem(i, 0, item)

            item = QTableWidgetItem(self.atlas.brain_regions[i].name)
            self.tableWidget.setItem(i, 1, item)

            item = QTableWidgetItem(str(self.atlas.brain_regions[i].x))
            self.tableWidget.setItem(i, 2, item)

            item = QTableWidgetItem(str(self.atlas.brain_regions[i].y))
            self.tableWidget.setItem(i, 3, item)

            item = QTableWidgetItem(str(self.atlas.brain_regions[i].z))
            self.tableWidget.setItem(i, 4, item)

        self.set_selected(selected)
        self.brainWidget.update_brain_regions(selected)

        self.tableWidget.blockSignals(False)
        if self.locked:
            self.set_locked(True)

    def region_selection_changed(self):
        selected = self.get_selected()
        self.brainWidget.deselect_all()
        for index in selected:
            self.brainWidget.select_region(index)

    def set_selected(self, selected):
        self.tableWidget.blockSignals(True)
        self.clear_selection()
        mode = self.tableWidget.selectionMode()
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for row in selected:
            self.tableWidget.selectRow(row)
        self.tableWidget.setSelectionMode(mode)
        self.tableWidget.blockSignals(False)

    def get_selected(self):
        rows = [item.row() for item in self.tableWidget.selectionModel().selectedRows()]
        return np.array(rows)

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "atlas files (*.atlas)")
        if file_name:
            self.file_name = file_name
            self.to_file(file_name)

    def save(self):
        if self.file_name:
            self.to_file(self.file_name)
        else:
            self.save_as()

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","atlas files (*.atlas)", options=options)
        if file_name:
            self.from_file(file_name)

    def set_cursor(self, file_name):
        cursor_file = abs_path_from_relative(__file__, file_name)
        pm = QtGui.QPixmap(cursor_file)
        cursor = QtGui.QCursor(pm)
        self.brainWidget.setCursor(cursor)

    def zoom_in(self):
        self.set_cursor('icons/zoom_in.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ZOOM_IN

    def zoom_out(self):
        self.set_cursor('icons/zoom_out.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT

    def pan_y(self):
        self.set_cursor('icons/hand_xy.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_PAN_Y

    def pan_z(self):
        self.set_cursor('icons/hand_xz.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_PAN_Z

    def rotate(self):
        self.set_cursor('icons/rotate.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ROTATE

    def find(self):
        self.set_cursor('icons/cursor.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_FIND


    def import_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","Atlas files (*.txt *.xml *.xlsx) ;; \
                                                          Text files (*.txt,);; \
                                                          xml files (*.xml);; \
                                                          xlsx files (*.xlsx", options=options)
        if file_name:
            extension = file_name.split(".")[-1]
            if extension == "txt":
                self.atlas.load_from_txt(file_name)
            elif extension == "xml":
                self.atlas.load_from_xml(file_name)
            elif extension == "xlsx":
                self.atlas.load_from_xlsx(file_name)
            self.update_table()

    def export_xml(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "xml files (*.xml)")
        if file_name:
            self.atlas.save_to_xml(file_name)

    def export_txt(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "txt files (*.txt)")
        if file_name:
            self.atlas.save_to_txt(file_name)

    def close(self):
        pass

    def brain_view_open(self):
        self.comboBox.setCurrentText('Open...')

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
