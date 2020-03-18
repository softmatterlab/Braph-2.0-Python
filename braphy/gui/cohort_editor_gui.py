import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.brain_atlas_widget import BrainAtlasWidget
from braphy.gui.brain_atlas_gui import BrainAtlasGui
import braphy.gui.icons_rc
from functools import partial
import xml.etree.ElementTree as ET
import numpy as np

from braphy.cohort.cohort import Cohort
from braphy.cohort.subjects.subject_MRI import SubjectMRI

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/cohort_editor.ui")
brain_mesh_file_name = "BrainMesh_ICBM152.nv"
brain_mesh_file = abs_path_from_relative(__file__, brain_mesh_file_name)

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
subject_class = SubjectMRI

class CohortEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, cohort = None):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        if cohort == None:
            self.cohort = Cohort('Cohort', subject_class)
        else:
            self.cohort = cohort
        self.setupUi(self)
        self.init_buttons()
        self.init_actions()
        self.init_table()
        self.init_brain_widget()

        self.atlas_loaded = False
        self.disable_menu_bar(True)
        self.set_brain_view_actions_visible(False)
        self.tab_groups_and_demographics()
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.group_radio_buttons = []
        self.subject_check_boxes = []

    def init_brain_widget(self):
        self.brainWidget.init_brain_view(brain_mesh_file)
        self.brainWidget.change_transparency(0.5)

    def init_table(self):
        header = self.tableWidget_groups.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        self.tableWidget_groups.setColumnWidth(0, 50)
        self.tableWidget_groups.setColumnWidth(1, 100)
        self.tableWidget_groups.setColumnWidth(2, 150)
        self.tableWidget_groups.setColumnWidth(3, 150)

    def init_buttons(self):
        self.btnAtlas.clicked.connect(self.btn_brain_atlas)

        self.btnLoadXls.clicked.connect(self.load_xls_subject_group)
        self.btnLoadTxt.clicked.connect(self.load_txt_subject_group)
        self.btnLoadXml.clicked.connect(self.load_xml_subject_group)

        self.btnAdd.clicked.connect(self.add_new_group)
        self.btnRemove.clicked.connect(self.remove_group)
        self.btnMoveUp.clicked.connect(self.move_group_up)
        self.btnMoveDown.clicked.connect(self.move_group_down)

        self.btnInvert.clicked.connect(self.invert_group)
        self.btnMerge.clicked.connect(self.merge_groups)
        self.btnIntersect.clicked.connect(self.intersect_groups)

        self.btnSelectAll.clicked.connect(self.select_all_subjects)
        self.btnClearSelection.clicked.connect(self.clear_subject_selection)
        self.btnAddSubject.clicked.connect(self.add_subject)
        self.btnAddAbove.clicked.connect(self.add_subjects_above)
        self.btnAddBelow.clicked.connect(self.add_subjects_below)
        self.btnRemove2.clicked.connect(self.remove_subjects)
        self.btnMoveUp2.clicked.connect(self.move_subjects_up)
        self.btnMoveDown2.clicked.connect(self.move_subjects_down)
        self.btnNewGroup.clicked.connect(self.new_group)

        self.btnSaveSubjects.clicked.connect(self.save_subjects)

        self.btnComparison.clicked.connect(self.comparison)

        self.btnViewSubjects.clicked.connect(self.view_subjects)
        self.btnViewGroup.clicked.connect(self.view_group)
        self.btnViewComparison.clicked.connect(self.view_comparison)

    def init_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionImport_xml.triggered.connect(self.import_xml)
        self.actionExport_xml.triggered.connect(self.export_xml)
        self.actionClose.triggered.connect(self.close)

        self.actionLoad_subject_group_from_xls.triggered.connect(self.load_xls_subject_group)
        self.actionLoad_subject_group_from_txt.triggered.connect(self.load_txt_subject_group)
        self.actionLoad_subject_group_from_xml.triggered.connect(self.load_xml_subject_group)
        self.actionAdd_group.triggered.connect(self.add_new_group)
        self.actionRemove_group.triggered.connect(self.remove_group)
        self.actionMove_group_up.triggered.connect(self.move_group_up)
        self.actionMove_group_down.triggered.connect(self.move_group_down)

        self.actionAdd_subject.triggered.connect(self.add_subject)
        self.actionAdd_subject_above.triggered.connect(self.add_subjects_above)
        self.actionAdd_subject_below.triggered.connect(self.add_subjects_below)
        self.actionRemove_subject.triggered.connect(self.remove_subjects)
        self.actionMove_subject_up.triggered.connect(self.move_subjects_up)
        self.actionMove_subject_down.triggered.connect(self.move_subjects_down)
        self.actionMove_subject_to_top.triggered.connect(self.move_subjects_to_top)
        self.actionMove_subject_to_bottom.triggered.connect(self.move_subjects_to_bottom)

        self.actionGroups_and_Demographics.triggered.connect(self.tab_groups_and_demographics)
        self.actionSubject_Data.triggered.connect(self.tab_subject_data)
        self.actionGroup_Averages.triggered.connect(self.tab_group_averages)
        self.actionBrain_View.triggered.connect(self.tab_brain_view)

        self.actionGenerate_figure.triggered.connect(self.brainWidget.generate_figure)

        self.actionNew_MRI_graph_analysis.triggered.connect(self.new_MRI_graph_analysis)

        self.actionAbout.triggered.connect(self.about)

        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPan.triggered.connect(self.pan)
        self.action3D_rotation.triggered.connect(self.rotation)
        self.actionData_cursor.triggered.connect(self.data_cursor)
        self.actionInsert_colorbar.triggered.connect(self.insert_colorbar)

        group = QtWidgets.QActionGroup(self, exclusive = True)
        for action in (self.actionZoom_in, self.actionZoom_out, self.actionPan,
                       self.action3D_rotation, self.actionData_cursor):
            group.addAction(action)

        self.action3D.triggered.connect(self.brainWidget.show_3D)
        self.actionSagittal_left.triggered.connect(self.brainWidget.sagittal_left)
        self.actionSagittal_right.triggered.connect(self.brainWidget.sagittal_right)
        self.actionAxial_dorsal.triggered.connect(self.brainWidget.axial_dorsal)
        self.actionAxial_ventral.triggered.connect(self.brainWidget.axial_ventral)
        self.actionCoronal_anterior.triggered.connect(self.brainWidget.coronal_anterior)
        self.actionCoronal_posterior.triggered.connect(self.brainWidget.coronal_posterior)

        self.actionShow_brain.triggered.connect(self.show_brain)
        self.actionShow_axis.triggered.connect(self.show_axis)
        self.actionShow_grid.triggered.connect(self.show_grid)
        self.actionShow_symbols.triggered.connect(self.show_symbols)
        self.actionShow_regions.triggered.connect(self.show_regions)
        self.actionShow_labels.triggered.connect(self.show_labels)

    def set_brain_view_actions_visible(self, state):
        self.actionZoom_in.setVisible(state)
        self.actionZoom_out.setVisible(state)
        self.actionPan.setVisible(state)
        self.action3D_rotation.setVisible(state)
        self.actionData_cursor.setVisible(state)
        self.actionInsert_colorbar.setVisible(state)
        self.action3D.setVisible(state)
        self.actionSagittal_left.setVisible(state)
        self.actionSagittal_right.setVisible(state)
        self.actionAxial_dorsal.setVisible(state)
        self.actionAxial_ventral.setVisible(state)
        self.actionCoronal_anterior.setVisible(state)
        self.actionCoronal_posterior.setVisible(state)
        self.actionShow_brain.setVisible(state)
        self.actionShow_axis.setVisible(state)
        self.actionShow_grid.setVisible(state)
        self.actionShow_symbols.setVisible(state)
        self.actionShow_regions.setVisible(state)
        self.actionShow_labels.setVisible(state)

        self.actionShow_brain.setChecked(state)

    def tab_changed(self):
        if self.tabWidget.currentIndex() == 3:
            self.set_brain_view_actions_visible(True)
        else:
            self.set_brain_view_actions_visible(False)

    def tab_groups_and_demographics(self):
        self.tabWidget.setCurrentIndex(0)

    def tab_subject_data(self):
        self.tabWidget.setCurrentIndex(1)

    def tab_group_averages(self):
        self.tabWidget.setCurrentIndex(2)

    def tab_brain_view(self):
        self.tabWidget.setCurrentIndex(3)

    def open(self):
        print("open")

    def save(self):
        pass

    def save_as(self):
        pass

    def import_xml(self):
        pass

    def export_xml(self):
        pass

    def close(self):
        pass

    def new_MRI_graph_analysis(self):
        pass

    def about(self):
        pass

    def set_cursor(self, file_name):
        cursor_file = abs_path_from_relative(__file__, file_name)
        pm = QtGui.QPixmap(cursor_file)
        cursor = QtGui.QCursor(pm)
        self.brainWidget.setCursor(cursor)

    def zoom_in(self):
        self.set_cursor('zoom_in.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ZOOM_IN

    def zoom_out(self):
        self.set_cursor('zoom_out.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT

    def pan(self):
        self.set_cursor('hand.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_PAN

    def rotation(self):
        self.set_cursor('rotate.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ROTATE

    def data_cursor(self):
        self.set_cursor('cursor.png')

    def insert_colorbar(self):
        pass

    def show_brain(self, state):
        self.brainWidget.show_brain(state)

    def show_axis(self, state):
        self.brainWidget.show_axis(state)

    def show_grid(self, state):
        self.brainWidget.show_grid(state)

    def show_symbols(self, state):
        pass

    def show_regions(self, state):
        pass

    def show_labels(self, state):
        self.brainWidget.show_labels(state)

    def btn_brain_atlas(self):
        if not self.atlas_loaded:
            self.load_atlas()
        else:
            self.brain_atlas_gui = BrainAtlasGui(self)
            self.brain_atlas_gui.set_locked(True)
            self.brain_atlas_gui.show()

    def load_atlas(self):
        print("Loading brain atlas...")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","atlas files (*.atlas)", options=options)
        if fileName:
            print(fileName)
            self.atlas_loaded = True
            self.btnAtlas.setText("View Atlas")
            self.disable_menu_bar(False)

    def load_xls_subject_group(self):
        print("Loading xls subject group...")

    def load_txt_subject_group(self):
        print("Loading txt subject group...")

    def load_xml_subject_group(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","xml files (*.xml)", options=options)
        if fileName:
            tree = ET.parse(fileName)
            root = tree.getroot()
            subjects = []
            for MRISubject in root[0].findall('MRISubject'):
                tmp_dict = {
                    "age": MRISubject.attrib["age"],
                    "code": MRISubject.attrib["code"],
                    "data": self.string_to_list_of_floats(MRISubject.attrib["data"]),
                    "gender": MRISubject.attrib["gender"],
                    "notes": MRISubject.attrib["notes"]
                }
                subjects.append(tmp_dict)
            group_data = {
                "data": self.string_to_list_of_ints(root[0][-1][0].attrib["data"]),
                "name": root[0][-1][0].attrib["name"],
                "notes": root[0][-1][0].attrib["notes"]
            }
            self.subjects = subjects
            self.group_data = group_data
            self.update_tables()

    def string_to_list_of_floats(self, str):
        string_list = str.split()
        float_list = []
        for i in string_list:
            float_list.append(float(i))
        return float_list

    def string_to_list_of_ints(self, str):
        string_list = str.split()
        float_list = []
        for i in string_list:
            float_list.append(int(i))
        return float_list

    def update_tables(self, selected_groups = None, selected_subjects = None):
        if np.any(selected_groups == None):
            selected_groups = self.get_checked_groups()
        if np.any(selected_subjects == None):
            selected_subjects = self.get_checked_subjects()

        self.update_group_table(selected_groups)
        self.update_groups_and_demographics_table(selected_subjects)
        self.update_subject_data_table()
        self.update_group_averages_table()

    def update_group_table(self, selected):
        self.tableWidget_groups.blockSignals(True)
        self.tableWidget_groups.clearContents()
        self.tableWidget_groups.setRowCount(0)
        self.group_radio_buttons = []

        for i in range(len(self.cohort.groups)):
            self.tableWidget_groups.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)
            radio_button = QRadioButton()
            #radio_button.stateChanged.connect(self.group_radio_button_changed)
            self.group_radio_buttons.append(radio_button)
            if i in selected:
                self.group_radio_buttons[i].setChecked(True)
            layout.addWidget(self.group_radio_buttons[i])
            widget.setLayout(layout)
            self.tableWidget_groups.setCellWidget(i, 0, widget)

            item = QTableWidgetItem(self.cohort.groups[i].name)
            self.tableWidget_groups.setItem(i, 1, item)

            item = QTableWidgetItem(str(len(self.cohort.groups[i].subjects)))
            self.tableWidget_groups.setItem(i, 2, item)

            item = QTableWidgetItem(self.cohort.groups[i].description)
            self.tableWidget_groups.setItem(i, 3, item)

        self.tableWidget_groups.blockSignals(False)

    def update_groups_and_demographics_table(self, selected):
        self.tableWidget_groups_and_demographics.blockSignals(True)
        self.tableWidget_groups_and_demographics.clearContents()
        self.tableWidget_groups_and_demographics.setRowCount(0)
        self.subject_check_boxes = []

        #Update columns:
        self.tableWidget_groups_and_demographics.setColumnCount(2)
        item = QTableWidgetItem('Subject Code')
        self.tableWidget_groups_and_demographics.setHorizontalHeaderItem(1, item)
        keys = self.cohort.subjects[0].data_dict.keys()
        for i in range(len(keys)):
            item = QTableWidgetItem(keys[i])
            self.tableWidget_groups_and_demographics.setHorizontalHeaderItem(i+2, item)

        # Update subjects:
        for i in range(len(self.cohort.subjects)):
            self.tableWidget_groups_and_demographics.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)
            check_box = QCheckBox()
            #radio_button.stateChanged.connect(self.group_radio_button_changed)
            self.subject_check_boxes.append(check_box)
            if i in selected:
                self.subject_check_boxes[i].setChecked(True)
            layout.addWidget(self.subject_check_boxes[i])
            widget.setLayout(layout)
            self.tableWidget_groups_and_demographics.setCellWidget(i, 0, widget)

            item = QTableWidgetItem(self.cohort.subjects[i].id)
            self.tableWidget_groups_and_demographics.setItem(i, 1, item)

            for j in range(len(keys)):
                item = QTableWidgetItem(str(self.cohort.subjects[i].data_dict[keys[j]]))
                self.tableWidget_groups_and_demographics.setItem(i, j+2, item)

        self.tableWidget_groups_and_demographics.blockSignals(False)

    def update_subject_data_table(self):
        pass

    def update_group_averages_table(self):
        pass

    def group_radio_button_changed(self):
        pass

    def get_checked_groups(self):
        selected = []
        for i in range(len(self.group_radio_buttons)):
            if self.group_radio_buttons[i].isChecked():
                selected.append(i)
        return np.array(selected)

    def get_checked_subjects(self):
        selected = []
        for i in range(len(self.subject_check_boxes)):
            if self.subject_check_boxes[i].isChecked():
                selected.append(i)
        return np.array(selected)

    def set_checked_subjects(self, selected):
        for i in range(len(self.subject_check_boxes)):
            if i in selected:
                self.subject_check_boxes[i].setChecked(True)
            else:
                self.subject_check_boxes[i].setChecked(False)

    def set_checked_groups(self, selected):
        for i in range(len(self.group_radio_buttons)):
            if i in selected:
                self.group_radio_buttons[i].setChecked(True)
            else:
                self.group_radio_buttons[i].setChecked(False)

    def disable_menu_bar(self, b):
        self.menuGroups.setDisabled(b)
        self.menuSubjects.setDisabled(b)
        self.menuView.setDisabled(b)
        self.menuBrain_View.setDisabled(b)
        self.menuGraph_Analysis.setDisabled(b)

    def add_new_group(self):
        self.cohort.add_new_group()
        self.update_tables(self.get_checked_groups())

    def remove_group(self):
        selected_groups = self.cohort.remove_groups(self.get_checked_groups())
        self.update_tables(selected_groups)

    def move_group_up(self):
        selected_groups = self.cohort.move_up_groups(self.get_checked_groups())
        self.update_tables(selected_groups)
    
    def move_group_down(self):
        selected_groups = self.cohort.move_down_groups(self.get_checked_groups())
        self.update_tables(selected_groups)

    def invert_group(self):
        print("invert")

    def merge_groups(self):
        print("merge")

    def intersect_groups(self):
        print("intersect")

    def select_all_subjects(self):
        for check_box in self.subject_check_boxes:
            check_box.setChecked(True)

    def clear_subject_selection(self):
        for check_box in self.subject_check_boxes:
            check_box.setChecked(False)

    def add_subject(self):
        self.cohort.add_subject()
        self.update_tables(self.get_checked_groups(), self.get_checked_subjects())

    def add_subjects_above(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects, added_subjects = self.cohort.add_above_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def add_subjects_below(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects, added_subjects = self.cohort.add_below_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def remove_subjects(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects = self.cohort.remove_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def move_subjects_up(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects = self.cohort.move_up_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def move_subjects_down(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects = self.cohort.move_down_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def move_subjects_to_top(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects = self.cohort.move_to_top_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def move_subjects_to_bottom(self):
        selected_subjects = self.get_checked_subjects()
        selected_subjects = self.cohort.move_to_bottom_subjects(selected_subjects)
        self.update_tables(self.get_checked_groups(), selected_subjects)

    def new_group(self):
        self.cohort.add_new_group()
        self.update_tables(self.get_checked_groups(), self.get_checked_subjects())

    def save_subjects(self):
        pass

    def comparison(self):
        pass

    def view_subjects(self):
        pass

    def view_group(self):
        pass

    def view_comparison(self):
        pass

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = CohortEditor()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
