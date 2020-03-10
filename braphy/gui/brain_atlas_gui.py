import sys
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
import numpy as np
from braphy.gui.brain_widget import BrainWidget

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/brain_atlas.ui")
brain_mesh_file_name = "BrainMesh_ICBM152.nv"
brain_mesh_file = abs_path_from_relative(__file__, brain_mesh_file_name)

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BrainAtlasGui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, atlas = None): # should be able to input atlas
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        if atlas == None:
            self.atlas = BrainAtlas(mesh_file = brain_mesh_file_name)
        else:
            self.atlas = atlas
        self.setupUi(self)
        self.brainWidget.init_brain_view(brain_mesh_file)
        self.brainWidget.init_brain_regions(self.atlas.brain_regions, self.actionShow_brain_regions.isChecked())
        self.init_buttons()
        self.init_check_boxes()
        self.init_actions()

        self.init_combo_box()
        self.init_slider()
        self.check_boxes = []
        self.tableWidget.cellChanged.connect(self.changeCell)

        self.textAtlasName.setText(self.atlas.name)
        self.meshName.setText('Brain View')
        self.textAtlasName.textChanged.connect(self.atlas_name_change)

    def init_combo_box(self):
        self.mesh_file_paths = []
        nv_files = self.get_all_nv_files()
        for file in nv_files:
            self.comboBox.addItem(file)
            self.mesh_file_paths.append(abs_path_from_relative(__file__, file))

        self.comboBox.insertSeparator(self.comboBox.count())
        self.comboBox.addItem('Open...')
        self.comboBox.currentIndexChanged.connect(self.select_brain_mesh)
        self.last_combobox_index = 0

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
            file_path = self.mesh_file_paths[i]
            self.last_combobox_index = i
        if file_path:
            self.brainWidget.change_brain_mesh(file_path)
            self.change_transparency()

    def get_all_nv_files(self):
        dir = abs_path_from_relative(__file__)
        nv_files = [f for f in os.listdir(dir) if f.endswith('.nv')]
        return nv_files

    def init_slider(self):
        self.horizontalSlider.valueChanged.connect(self.change_transparency)
        self.horizontalSlider.setValue(50)

    def change_transparency(self):
        alpha = self.horizontalSlider.value()/100.0
        self.brainWidget.change_transparency(alpha)

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
        self.actionPan.triggered.connect(self.pan)
        self.actionRotate.triggered.connect(self.rotate)
        self.actionFind.triggered.connect(self.find)

        group = QtWidgets.QActionGroup(self, exclusive = True)
        for action in (self.actionZoom_in, self.actionZoom_out, self.actionPan,
                       self.actionRotate, self.actionFind):
            group.addAction(action)

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

        self.actionGenerate_figure.triggered.connect(self.brainWidget.generate_figure)
        self.actionBrainViewOpen.triggered.connect(self.brain_view_open)

        self.actionNew_MRI_Cohort.triggered.connect(self.new_mri_cohort)
        self.actionNew_fMRI_Cohort.triggered.connect(self.new_fmri_cohort)
        self.actionNew_EEG_Cohort.triggered.connect(self.new_eeg_cohort)
        self.actionNew_PET_Cohort.triggered.connect(self.new_pet_cohort)

        self.actionAbout.triggered.connect(self.about)

    def init_check_boxes(self):
        self.checkBoxShowBrain.stateChanged.connect(self.show_brain)
        self.checkBoxShowBrain.setChecked(True)
        self.checkBoxShowAxis.stateChanged.connect(self.show_axis)
        self.checkBoxShowAxis.setChecked(True)
        self.checkBoxShowGrid.stateChanged.connect(self.show_grid)
        self.checkBoxShowGrid.setChecked(True)
        self.checkBoxShowBrainRegions.stateChanged.connect(self.show_brain_regions)
        self.checkBoxShowBrainRegions.setChecked(True)
        self.checkBoxShowLabels.stateChanged.connect(self.show_labels)
        self.checkBoxShowLabels.setChecked(True)

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
            self.brainWidget.show_brain_regions(state)
            self.actionShow_brain_regions.setChecked(state != 0)
            self.checkBoxShowBrainRegions.setChecked(state != 0)

    def show_labels(self, state):
        if (self.actionShow_labels.isChecked() != self.checkBoxShowLabels.isChecked()):
            self.brainWidget.show_labels(state)
            self.actionShow_labels.setChecked(state != 0)
            self.checkBoxShowLabels.setChecked(state != 0)

    def select_all(self):
        selected = np.arange(len(self.atlas.brain_regions))
        self.set_checked(selected)

    def clear_selection(self):
        self.set_checked(np.array([]))

    def add(self):
        self.atlas.add_brain_region()
        self.update_table()

    def add_above(self):
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

    def atlas_name_change(self):
        self.atlas.name = self.textAtlasName.toPlainText()

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
            check_box.stateChanged.connect(self.check_box_changed)
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

        self.brainWidget.update_brain_regions()
        self.tableWidget.blockSignals(False)

    def check_box_changed(self, state):
        check_box = self.sender()
        index = self.check_boxes.index(check_box)
        if state == 0:
            self.brainWidget.deselect_region(index)
        else:
            self.brainWidget.select_region(index)

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

    def set_cursor(self, file_name):
        cursor_file = abs_path_from_relative(__file__, file_name)
        pm = QtGui.QPixmap(cursor_file)
        cursor = QtGui.QCursor(pm)
        self.brainWidget.setCursor(cursor)

    def zoom_in(self):
        self.set_cursor('zoom_in.png')

    def zoom_out(self):
        self.set_cursor('zoom_out.png')

    def pan(self):
        self.set_cursor('hand.png')

    def rotate(self):
        self.set_cursor('rotate.png')

    def find(self):
        self.set_cursor('cursor.png')

    def show_3D(self):
        pass

    def save_as(self):
        pass

    def import_txt(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","txt files (*.txt)", options=options)
        self.atlas.load_from_txt(file_name)
        self.update_table()

    def import_xls(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","xls files (*.xls)", options=options)
        self.atlas.load_from_xls(file_name)
        self.update_table()

    def import_xml(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","xml files (*.xml)", options=options)
        self.atlas.load_from_xml(file_name)
        self.update_table()

    def export_xml(self):
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "xml files (*.xml)")
        if file_name:
            self.atlas.save_to_xml(file_name)

    def export_txt(self):
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
