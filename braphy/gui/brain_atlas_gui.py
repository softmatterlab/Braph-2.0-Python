import sys
import os
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.utility.helper_functions import abs_path_from_relative, load_nv, FloatDelegate, float_to_string
import numpy as np
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget
from braphy.workflows import *

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
        self.init_brain_widget(brain_mesh_file_default)
        self.settingsWidget.init(self.brainWidget)
        self.init_combo_boxes()
        self.init_buttons()
        self.init_actions()
        self.init_table()

        self.textAtlasName.setText(self.atlas.name)
        self.meshName.setText('Brain View')
        self.textAtlasName.textChanged.connect(self.atlas_name_change)
        self.file_name = None
        self.loaded_mesh_data = None
        self.brainWidget.add_selected_observer(self.set_selected)
        self.update_table()

        if not AppWindow:
            self.actionNew_MRI_Cohort.setEnabled(False)
            self.actionNew_fMRI_Cohort.setEnabled(False)
            self.actionNew_EEG_Cohort.setEnabled(False)
            self.actionNew_PET_Cohort.setEnabled(False)

    def to_file(self, atlas_file):
        with open(atlas_file, 'w') as f:
            json.dump(self.to_dict(), f, sort_keys=True, indent=4)

    def to_dict(self):
        d = {}
        d['atlas'] = self.atlas.to_dict()
        brain_mesh_data = {}
        brain_mesh_data['vertices'] = self.brain_mesh_data['vertices'].tolist()
        brain_mesh_data['faces'] = self.brain_mesh_data['faces'].tolist()
        d['brain_mesh_data'] = brain_mesh_data
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
        self.add_mesh_to_combobox(self.atlas.mesh_file)
        self.loaded_mesh_data = (self.atlas.mesh_file, brain_mesh_data)
        self.update_table()

    def add_mesh_to_combobox(self, mesh_file_name):
        self.comboBoxMeshFile.blockSignals(True)
        idx = self.comboBoxMeshFile.findText(mesh_file_name)
        if idx > -1:
            self.comboBoxMeshFile.setCurrentIndex(idx)
        else:
            self.comboBoxMeshFile.insertItem(self.comboBoxMeshFile.count() - 2, mesh_file_name)
            self.comboBoxMeshFile.setCurrentText(mesh_file_name)
        self.comboBoxMeshFile.blockSignals(False)

    def set_brain_mesh_file(self, brain_mesh_file):
        self.brain_mesh_file_name = brain_mesh_file.split('/')[-1]
        self.atlas.mesh_file = self.brain_mesh_file_name
        self.brain_mesh_data = load_nv(brain_mesh_file)
        self.set_brain_mesh_data()

    def set_brain_mesh_data(self):
        self.settingsWidget.checkBoxShowBrain.setChecked(True)
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.settingsWidget.change_transparency()

    def set_brain_regions(self):
        size = self.settingsWidget.sliderRegions.value()/10.0
        show_only_selected = self.settingsWidget.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.settingsWidget.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.atlas.brain_regions, size, self.get_selected(), show_brain_regions, show_only_selected)

    def init_brain_widget(self, brain_mesh_file):
        self.brain_mesh_file_name = brain_mesh_file.split('/')[-1]
        self.brain_mesh_data = load_nv(brain_mesh_file)
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.set_brain_regions()

    def init_combo_boxes(self):
        self.mesh_file_paths = []
        nv_files = self.get_all_nv_files()
        for file in nv_files:
            self.comboBoxMeshFile.addItem(file)
            self.mesh_file_paths.append(abs_path_from_relative(__file__, 'meshes/{}'.format(file)))

        self.comboBoxMeshFile.insertSeparator(self.comboBoxMeshFile.count())
        self.comboBoxMeshFile.addItem('Open...')
        idx = self.comboBoxMeshFile.findText(self.brain_mesh_file_name)
        self.comboBoxMeshFile.setCurrentIndex(idx)
        self.comboBoxMeshFile.currentIndexChanged.connect(self.select_brain_mesh)
        self.last_combobox_index = idx

    def set_locked(self, locked):
        self.locked = locked
        lock_items = [self.comboBoxMeshFile, self.textAtlasName, self.actionOpen, self.actionImport_file,
                      self.btnAdd, self.btnAddAbove, self.btnAddBelow, self.btnRemove,
                      self.actionAdd, self.actionAdd_above, self.actionAdd_below, self.actionRemove,
                      self.actionBrainViewOpen, self.menuSubject_Cohorts]
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
        if self.comboBoxMeshFile.currentText() == 'Open...':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, name = QFileDialog.getOpenFileName(self, "Select brain mesh",
                                                      "","nv files (*.nv)", options = options)
            if file_path:
                file_name = file_path.split('/')[-1]
                self.comboBoxMeshFile.blockSignals(True)
                self.comboBoxMeshFile.insertItem(self.comboBoxMeshFile.count() - 2, file_name)
                self.comboBoxMeshFile.setCurrentText(file_name)
                self.comboBoxMeshFile.blockSignals(False)
                self.mesh_file_paths.append(file_path)
                self.last_combobox_index = self.comboBoxMeshFile.count() - 3
            else:
                self.comboBoxMeshFile.blockSignals(True)
                self.comboBoxMeshFile.setCurrentIndex(self.last_combobox_index)
                self.comboBoxMeshFile.blockSignals(False)
        else:
            if self.loaded_mesh_data:
                if i == self.comboBoxMeshFile.findText(self.loaded_mesh_data[0]):
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

    def init_buttons(self):
        self.btnSelectAll.clicked.connect(self.tableWidget.selectAll)
        self.btnClearSelection.clicked.connect(self.tableWidget.clearSelection)
        self.btnAdd.clicked.connect(self.add)
        self.btnAddAbove.clicked.connect(self.add_above)
        self.btnAddBelow.clicked.connect(self.add_below)
        self.btnRemove.clicked.connect(self.remove)
        self.btnMoveUp.clicked.connect(self.move_up)
        self.btnMoveDown.clicked.connect(self.move_down)
        self.btnMoveToTop.clicked.connect(self.move_to_top)
        self.btnMoveToBottom.clicked.connect(self.move_to_bottom)

    def init_actions(self):
        # TOOL BAR:
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.open)
        self.toolBar.addSeparator()

        for action in self.brainWidget.get_actions():
             self.toolBar.addAction(action)
        self.toolBar.addSeparator()

        for action in self.settingsWidget.get_actions():
            self.toolBar.addAction(action)

        # MENU BAR:
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionImport_file.triggered.connect(self.import_file)
        self.actionExport_xml.triggered.connect(lambda state, file_type = 'xml', save_to_function = self.atlas.save_to_xml: self.export(file_type, save_to_function))
        self.actionExport_txt.triggered.connect(lambda state, file_type = 'txt', save_to_function = self.atlas.save_to_txt: self.export(file_type, save_to_function))
        self.actionExport_xlsx.triggered.connect(lambda state, file_type = 'xlsx', save_to_function = self.atlas.save_to_xlsx: self.export(file_type, save_to_function))
        self.actionQuit.triggered.connect(self.close)

        self.actionSelect_all.triggered.connect(self.tableWidget.selectAll)
        self.actionClear_selection.triggered.connect(self.tableWidget.clearSelection)
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

    def init_table(self):
        self.tableWidget.cellChanged.connect(self.change_cell)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.itemSelectionChanged.connect(self.region_selection_changed)
        for column in [2, 3, 4]:
            self.tableWidget.setItemDelegateForColumn(column, FloatDelegate(self.tableWidget))

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

    def update_table(self, selected = None):
        if np.any(selected == None):
            selected = self.get_selected()

        self.tableWidget.blockSignals(True)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(self.atlas.brain_region_number())

        for i in range(self.atlas.brain_region_number()):
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)

            item = QTableWidgetItem(self.atlas.brain_regions[i].label)
            self.tableWidget.setItem(i, 0, item)

            item = QTableWidgetItem(self.atlas.brain_regions[i].name)
            self.tableWidget.setItem(i, 1, item)

            item = QTableWidgetItem(float_to_string(self.atlas.brain_regions[i].x))
            self.tableWidget.setItem(i, 2, item)

            item = QTableWidgetItem(float_to_string(self.atlas.brain_regions[i].y))
            self.tableWidget.setItem(i, 3, item)

            item = QTableWidgetItem(float_to_string(self.atlas.brain_regions[i].z))
            self.tableWidget.setItem(i, 4, item)

        self.set_selected(selected)
        self.brainWidget.update_brain_regions(selected)

        self.tableWidget.blockSignals(False)
        if self.locked:
            self.set_locked(True)

        self.textAtlasName.blockSignals(True)
        self.textAtlasName.setText(self.atlas.name)
        self.textAtlasName.blockSignals(False)
        if self.comboBoxMeshFile.findText(self.atlas.mesh_file) != -1:
            self.comboBoxMeshFile.setCurrentText(self.atlas.mesh_file)
        else:
            self.load_file_warning('The brain mesh file {} could not be found in the repository. ' \
                                   'Try loading it from your computer and select \nit in the drop-' \
                                   'down menu.'.format(self.atlas.mesh_file))

    def region_selection_changed(self):
        selected = self.get_selected()
        self.brainWidget.deselect_all()
        for index in selected:
            self.brainWidget.select_region(index)

    def set_selected(self, selected):
        self.tableWidget.blockSignals(True)
        self.tableWidget.clearSelection()
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
        file_name, name = QFileDialog.getSaveFileName(self, "Save brain atlas", "untitled.atlas",
                                                      "atlas files (*.atlas)", options = options)
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
        file_name, name = QFileDialog.getOpenFileName(self,"Open brain atlas",
                                                      "","atlas files (*.atlas)", options = options)
        if file_name:
            self.from_file(file_name)

    def import_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"Import brain atlas",
                                                      "","Atlas files (*.txt *.xml *.xlsx) ;; \
                                                          Text files (*.txt,);; \
                                                          xml files (*.xml);; \
                                                          xlsx files (*.xlsx", options = options)
        if file_name:
            try:
                extension = file_name.split(".")[-1]
                if extension == "txt":
                    self.atlas.load_from_txt(file_name)
                elif extension == "xml":
                    self.atlas.load_from_xml(file_name)
                elif extension == "xlsx":
                    self.atlas.load_from_xlsx(file_name)
                self.update_table()
            except Exception as e:
                self.load_file_error(str(e))

    def export(self, file_type, save_to_function):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "Export brain atlas",
                                                      "untitled_atlas.{}".format(file_type),
                                                      "{} files (*.{})".format(file_type, file_type),
                                                      options = options)
        if file_name:
            save_to_function(file_name)

    def brain_view_open(self):
        self.comboBoxMeshFile.setCurrentText('Open...')

    def new_mri_cohort(self):
        self.AppWindow.cohort(atlas = self.atlas, brain_mesh_data = self.brain_mesh_data, subject_class = SubjectMRI)

    def new_fmri_cohort(self):
        self.AppWindow.cohort(atlas = self.atlas, brain_mesh_data = self.brain_mesh_data, subject_class = SubjectfMRI)

    def new_eeg_cohort(self):
        pass

    def new_pet_cohort(self):
        pass

    def about(self):
        QMessageBox.about(self, 'About', 'Brain Atlas Editor')

    def load_file_error(self, exception):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(str(exception))
        msg_box.setWindowTitle("Import error")
        msg_box.exec_()

    def load_file_warning(self, string):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(string)
        msg_box.setWindowTitle("Import warning")
        msg_box.exec_()

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = BrainAtlasGui()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
