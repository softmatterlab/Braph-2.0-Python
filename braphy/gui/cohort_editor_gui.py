import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
from braphy.gui.brain_atlas_widget import BrainAtlasWidget
from braphy.gui.brain_atlas_gui import BrainAtlasGui
from braphy.atlas.brain_region import BrainRegion
import braphy.gui.icons_rc
from functools import partial
import xml.etree.ElementTree as ET
import numpy as np

from braphy.cohort.cohort import Cohort
from braphy.cohort.subjects.subject_MRI import SubjectMRI

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/cohort_editor.ui")
brain_mesh_file_name_default = "BrainMesh_ICBM152.nv"
brain_mesh_file_default = abs_path_from_relative(__file__, brain_mesh_file_name_default)

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
subject_class = SubjectMRI

class CohortEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None, cohort = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        if cohort == None:
            self.cohort = Cohort('Cohort', subject_class)
        else:
            self.cohort = cohort
        self.setupUi(self)
        fMRI = False
        if fMRI:
            self.tabWidget.tabBar().setTabEnabled(2, False)
            self.tabWidget.tabBar().setTabEnabled(3, False)
            self.tabWidget.tabBar().setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        else:
            self.listSubjects.hide()
        self.brain_mesh_data = load_nv(brain_mesh_file_default)
        self.init_buttons()
        self.init_actions()
        self.init_table()
        self.init_brain_widget()

        self.atlas_dict = None
        self.file_name = None
        self.selected_groups_radio_button = None
        self.subject_data_labels = []
        self.disable_menu_bar(True)
        self.set_brain_view_actions_visible(False)
        self.tab_groups_and_demographics()
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.subject_check_boxes = []
        self.subject_in_group_check_boxes = {}

        self.tableWidget_groups.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_groups.itemSelectionChanged.connect(self.update_group_operation_buttons)
        self.tableWidget_groups.cellChanged.connect(self.cell_changed_in_group_table)
        self.tableWidget_groups_and_demographics.cellChanged.connect(self.cell_changed_in_groups_and_demographics_table)
        self.tableWidget_subject_data.cellChanged.connect(self.cell_changed_in_subject_data_table)

    def init_brain_widget(self):
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.brainWidget.change_transparency(0.5)

    def init_table(self):
        header = self.tableWidget_groups.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        self.tableWidget_groups.setColumnWidth(0, 100)
        self.tableWidget_groups.setColumnWidth(1, 150)
        self.tableWidget_groups.setColumnWidth(2, 150)

    def init_buttons(self):
        self.btnSelectAtlas.clicked.connect(self.load_atlas)
        self.btnViewAtlas.clicked.connect(self.view_atlas)

        self.btnLoadSubject.clicked.connect(self.load_subject_group)

        self.btnAdd.clicked.connect(self.add_group)
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
        self.btnMoveToTop.clicked.connect(self.move_subjects_to_top)
        self.btnMoveToBottom.clicked.connect(self.move_subjects_to_bottom)
        self.btnNewGroup.clicked.connect(self.new_group_from_selected)

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

        self.actionLoad_subject_group_from_file.triggered.connect(self.load_subject_group)
        self.actionAdd_group.triggered.connect(self.add_group)
        self.actionRemove_group.triggered.connect(self.remove_group)
        self.actionMove_group_up.triggered.connect(self.move_group_up)
        self.actionMove_group_down.triggered.connect(self.move_group_down)
        self.actionInvert.triggered.connect(self.invert_group)
        self.actionMerge.triggered.connect(self.merge_groups)
        self.actionIntersect.triggered.connect(self.intersect_groups)

        self.actionInvert.setEnabled(False)
        self.actionMerge.setEnabled(False)
        self.actionIntersect.setEnabled(False)

        self.actionSelect_all_subjects.triggered.connect(self.select_all_subjects)
        self.actionClear_selection.triggered.connect(self.clear_subject_selection)
        self.actionAdd_subject.triggered.connect(self.add_subject)
        self.actionAdd_subject_above.triggered.connect(self.add_subjects_above)
        self.actionAdd_subject_below.triggered.connect(self.add_subjects_below)
        self.actionRemove_subject.triggered.connect(self.remove_subjects)
        self.actionMove_subject_up.triggered.connect(self.move_subjects_up)
        self.actionMove_subject_down.triggered.connect(self.move_subjects_down)
        self.actionMove_subject_to_top.triggered.connect(self.move_subjects_to_top)
        self.actionMove_subject_to_bottom.triggered.connect(self.move_subjects_to_bottom)
        self.actionNew_group_from_selection.triggered.connect(self.new_group_from_selected)

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

        group = QtWidgets.QActionGroup(self)
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
        self.actionShow_regions.setVisible(state)
        self.actionShow_labels.setVisible(state)

    def update_group_operation_buttons(self):
        checked_groups = len(self.get_checked_groups())
        self.btnInvert.setEnabled(checked_groups > 0)
        self.actionInvert.setEnabled(checked_groups > 0)
        self.btnMerge.setEnabled(checked_groups > 1)
        self.actionMerge.setEnabled(checked_groups > 1)
        self.btnIntersect.setEnabled(checked_groups > 1)
        self.actionIntersect.setEnabled(checked_groups > 1)

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

    def cell_changed_in_group_table(self, row, column):
        if column == 1: # name
            self.cohort.groups[row].name = self.tableWidget_groups.item(row, column).text()
        elif column == 3: # notes
            self.cohort.groups[row].description = self.tableWidget_groups.item(row, column).text()
        self.update_tables()

    def cell_changed_in_groups_and_demographics_table(self, row, column):
        if column == 0: # check box
            pass
        elif column == 1: # subject code
            self.cohort.subjects[row].id = self.tableWidget_groups_and_demographics.item(row, column).text()
        else: # scalar data
            column_header = self.tableWidget_groups_and_demographics.horizontalHeaderItem(column).text()
            new_value = float(self.tableWidget_groups_and_demographics.item(row, column).text())
            self.cohort.subjects[row].data_dict[column_header].value = new_value
        self.update_subject_data_table()

    def cell_changed_in_subject_data_table(self, row, column):
        if column == 0: # subject code
            self.cohort.subjects[row].id = self.tableWidget_subject_data.item(row, column).text()
        else: # data
            new_value = float(self.tableWidget_subject_data.item(row, column).text())
            self.cohort.subjects[row].data_dict['data'].value[column-1] = new_value
        self.update_tables()

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","cohort files (*.cohort)", options=options)
        if file_name:
            self.cohort = Cohort.from_file(file_name)
            self.update_tables()

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "cohort files (*.cohort)")
        if file_name:
            self.file_name = file_name
            self.cohort.to_file(file_name)

    def save(self):
        if self.file_name:
            self.cohort.to_file(self.file_name)
        else:
            self.save_as()

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

    def show_regions(self, state):
        self.brainWidget.set_brain_regions_visible(state != 0)

    def show_labels(self, state):
        self.brainWidget.show_labels(state)

    def view_atlas(self):
        if self.atlas_dict:
            self.brain_atlas_gui = BrainAtlasGui(self, atlas_dict = self.atlas_dict)
            self.brain_atlas_gui.set_locked(True)
            self.brain_atlas_gui.show()

    def brain_region_number(self):
        n = 0
        if self.atlas_dict:
            n = len(self.atlas_dict['atlas']['brain_regions'])
        return n

    def load_atlas(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","atlas files (*.atlas)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                self.atlas_dict = json.load(f)
            vertices = np.asarray(self.atlas_dict['brain_mesh_data']['vertices'])
            faces = np.asarray(self.atlas_dict['brain_mesh_data']['faces'])
            brain_mesh_data = {'vertices': vertices, 'faces': faces}
            self.brain_mesh_data = brain_mesh_data
            self.init_brain_widget()
            self.subject_data_labels = []
            brain_regions = []
            for region in self.atlas_dict['atlas']['brain_regions']:
                self.subject_data_labels.append(region['label'])
                brain_regions.append(BrainRegion.from_dict(region))
            self.update_tables()
            self.btnViewAtlas.setEnabled(True)
            self.labelAtlasName.setText(file_name.split('/')[-1])
            self.labelRegionNumber.setText("Brain region number = {}".format(self.brain_region_number()))
            self.disable_menu_bar(False)
            self.brainWidget.init_brain_regions(brain_regions, 4, [], False, False)

    def load_subject_group(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","Subject files (*.txt *.xml *.xlsx);; \
                                                                                               Text files (*.txt);; \
                                                                                               XML files (*.xml);; \
                                                                                               XLSX files (*.xlsx)", options=options)
        for file_name in file_names:
            extension = file_name.split(".")[-1]
            if extension == "txt":
                self.cohort.load_from_txt(file_name)
            elif extension == "xml":
                self.cohort.load_from_xml(file_name)
            elif extension == "xlsx":
                self.cohort.load_from_xlsx(file_name)
        if len(file_names) > 0:
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
        self.update_group_comparison_table()
        self.update_group_averages_table()

    def update_group_table(self, selected_groups = None):
        if np.any(selected_groups == None):
            selected_groups = self.get_checked_groups()
        self.tableWidget_groups.blockSignals(True)
        self.tableWidget_groups.clearContents()
        self.tableWidget_groups.setRowCount(0)

        for i in range(len(self.cohort.groups)):
            self.tableWidget_groups.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)

            item = QTableWidgetItem(self.cohort.groups[i].name)
            self.tableWidget_groups.setItem(i, 0, item)

            item = QTableWidgetItem(str(len(self.cohort.groups[i].subjects)))
            self.tableWidget_groups.setItem(i, 1, item)

            item = QTableWidgetItem(self.cohort.groups[i].description)
            self.tableWidget_groups.setItem(i, 2, item)

        self.set_checked_groups(selected_groups)
        self.tableWidget_groups.blockSignals(False)

    def update_groups_and_demographics_table(self, selected):
        self.tableWidget_groups_and_demographics.blockSignals(True)
        self.tableWidget_groups_and_demographics.clearContents()
        self.tableWidget_groups_and_demographics.setRowCount(0)
        self.subject_check_boxes = []
        self.subject_in_group_check_boxes = {}

        #Update columns:
        self.tableWidget_groups_and_demographics.setColumnCount(2)
        item = QTableWidgetItem('Subject Code')
        self.tableWidget_groups_and_demographics.setHorizontalHeaderItem(1, item)
        try:
            keys = list(self.cohort.subjects[0].data_dict.keys())
        except:
            keys = []
        for i in range(len(keys)):
            if keys[i] == 'data':
                continue
            item = QTableWidgetItem(keys[i])
            self.tableWidget_groups_and_demographics.setColumnCount(i+3)
            self.tableWidget_groups_and_demographics.setHorizontalHeaderItem(i+2, item)

        nbr_columns = self.tableWidget_groups_and_demographics.columnCount()
        for i in range(len(self.cohort.groups)):
            item = QTableWidgetItem(self.cohort.groups[i].name)
            self.tableWidget_groups_and_demographics.setColumnCount(nbr_columns+i+1)
            self.tableWidget_groups_and_demographics.setHorizontalHeaderItem(nbr_columns+i, item)
            self.subject_in_group_check_boxes[self.cohort.groups[i]] = []

        # Update subjects:
        for i in range(len(self.cohort.subjects)):
            self.tableWidget_groups_and_demographics.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)
            check_box = QCheckBox()
            self.subject_check_boxes.append(check_box)
            if i in selected:
                self.subject_check_boxes[i].setChecked(True)
            layout.addWidget(self.subject_check_boxes[i])
            widget.setLayout(layout)
            self.tableWidget_groups_and_demographics.setCellWidget(i, 0, widget)

            item = QTableWidgetItem(self.cohort.subjects[i].id)
            self.tableWidget_groups_and_demographics.setItem(i, 1, item)

            for j in range(len(keys)):
                if keys[j] == 'data':
                    continue
                item = QTableWidgetItem(str(self.cohort.subjects[i].data_dict[keys[j]].value))
                self.tableWidget_groups_and_demographics.setItem(i, j+2, item)

            for j in range(len(self.cohort.groups)):
                widget = QWidget()
                layout = QHBoxLayout()
                layout.setAlignment(QtCore.Qt.AlignHCenter)
                check_box = QCheckBox()
                check_box.i = i
                check_box.j = j
                self.subject_in_group_check_boxes[self.cohort.groups[j]].append(check_box)
                self.subject_in_group_check_boxes[self.cohort.groups[j]][i].stateChanged.connect(self.subject_in_group_check_box_changed)
                if self.cohort.subjects[i] in self.cohort.groups[j].subjects:
                    self.subject_in_group_check_boxes[self.cohort.groups[j]][i].blockSignals(True)
                    self.subject_in_group_check_boxes[self.cohort.groups[j]][i].setChecked(True)
                    self.subject_in_group_check_boxes[self.cohort.groups[j]][i].blockSignals(False)
                layout.addWidget(self.subject_in_group_check_boxes[self.cohort.groups[j]][i])
                widget.setLayout(layout)
                self.tableWidget_groups_and_demographics.setCellWidget(i, nbr_columns+j, widget)

        self.tableWidget_groups_and_demographics.blockSignals(False)

    def subject_in_group_check_box_changed(self):
        check_box = self.sender()
        if check_box.isChecked():
            self.cohort.groups[check_box.j].add_subject(self.cohort.subjects[check_box.i])
        else:
            self.cohort.groups[check_box.j].remove_subject(self.cohort.subjects[check_box.i])
        self.update_group_table()
        self.update_group_comparison_table()

    def update_subject_data_table(self):
        self.tableWidget_subject_data.blockSignals(True)
        self.tableWidget_subject_data.clearContents()
        self.tableWidget_subject_data.setRowCount(0)

        #Update columns:
        self.tableWidget_subject_data.setColumnCount(len(self.subject_data_labels)+1)
        for i, label in enumerate(self.subject_data_labels):
            item = QTableWidgetItem(label)
            self.tableWidget_subject_data.setHorizontalHeaderItem(i+1, item)

        # Update subjects:
        for i in range(len(self.cohort.subjects)):
            self.tableWidget_subject_data.setRowCount(i+1)
            item = QTableWidgetItem(self.cohort.subjects[i].id)
            self.tableWidget_subject_data.setItem(i, 0, item)

            for j in range(len(self.cohort.subjects[i].data_dict['data'].value)):
                item = QTableWidgetItem(str(self.cohort.subjects[i].data_dict['data'].value[j]))
                self.tableWidget_subject_data.setItem(i, j+1, item)

        self.tableWidget_subject_data.blockSignals(False)

    def update_group_averages_table(self):
        self.tableWidget_group_averages.setColumnCount(len(self.subject_data_labels))
        self.tableWidget_group_averages.setHorizontalHeaderLabels(self.subject_data_labels)
        self.tableWidget_group_averages.setRowCount(len(self.cohort.groups)*2)
        for i, group in enumerate(self.cohort.groups):
            item = QTableWidgetItem("Average {}".format(group.name))
            self.tableWidget_group_averages.setVerticalHeaderItem((2*i), item)
            averages = group.averages()
            for j in range(len(averages)):
                item = QTableWidgetItem(str(averages[j]))
                self.tableWidget_group_averages.setItem(2*i, j, item)

            item = QTableWidgetItem("Std {}".format(group.name))
            self.tableWidget_group_averages.setVerticalHeaderItem((2*i+1), item)
            stds = group.standard_deviations()
            for j in range(len(stds)):
                item = QTableWidgetItem(str(stds[j]))
                self.tableWidget_group_averages.setItem(2*i+1, j, item)

    def update_group_comparison_table(self):
        self.tableWidget_group_comparison.setColumnCount(len(self.subject_data_labels))
        self.tableWidget_group_comparison.setHorizontalHeaderLabels(self.subject_data_labels)

        self.tableWidget_group_comparison_select.blockSignals(True)
        self.tableWidget_group_comparison_select.clearContents()

        group_names = [group.name for group in self.cohort.groups]
        self.tableWidget_group_comparison_select.setRowCount(len(group_names))
        self.tableWidget_group_comparison_select.setColumnCount(len(group_names))
        self.tableWidget_group_comparison_select.setVerticalHeaderLabels(group_names)
        self.tableWidget_group_comparison_select.setHorizontalHeaderLabels(group_names)

        self.selected_groups_radio_button = None

        for i, group1 in enumerate(self.cohort.groups):
            for j, group2 in enumerate(self.cohort.groups):
                if i == j:
                    item = QTableWidgetItem(" ")
                    item.setBackground(QtCore.Qt.lightGray)
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    self.tableWidget_group_comparison_select.setItem(i, j, item)
                else:
                    widget = QWidget()
                    layout = QHBoxLayout()
                    layout.setAlignment(QtCore.Qt.AlignHCenter)
                    radio_button = QRadioButton()
                    radio_button.toggled.connect(self.group_average_select_toggled)
                    radio_button.group1 = group1
                    radio_button.group2 = group2
                    layout.addWidget(radio_button)
                    widget.setLayout(layout)
                    self.tableWidget_group_comparison_select.setCellWidget(i, j, widget)

    def group_average_select_toggled(self, checked):
        if not checked:
            self.selected_groups_radio_button = None
            self.btnComparison.setEnabled(False)
        else:
            if self.selected_groups_radio_button:
                self.selected_groups_radio_button.setChecked(False)
            self.selected_groups_radio_button = self.sender()
            self.btnComparison.setEnabled(True)

    def set_checked_groups(self, selected):
        mode = self.tableWidget_groups.selectionMode()
        self.tableWidget_groups.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for row in selected:
            self.tableWidget_groups.selectRow(row)
        self.tableWidget_groups.setSelectionMode(mode)

    def get_checked_groups(self):
        rows = [item.row() for item in self.tableWidget_groups.selectionModel().selectedRows()]
        return np.array(rows)

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

    def disable_menu_bar(self, b):
        self.menuGroups.setDisabled(b)
        self.menuSubjects.setDisabled(b)
        self.menuView.setDisabled(b)
        self.menuBrain_View.setDisabled(b)
        self.menuGraph_Analysis.setDisabled(b)

    def add_group(self):
        self.cohort.add_group()
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
        self.cohort.invert_groups(self.get_checked_groups())
        self.update_tables()

    def merge_groups(self):
        self.cohort.merge_groups(self.get_checked_groups())
        self.update_tables()

    def intersect_groups(self):
        self.cohort.intersect_groups(self.get_checked_groups())
        self.update_tables()

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
        self.cohort.remove_subjects_from_all_groups(selected_subjects)
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

    def new_group_from_selected(self):
        selected_subjects = self.get_checked_subjects()
        self.cohort.new_group_from_selected(selected_subjects)
        self.update_tables(self.get_checked_groups(), self.get_checked_subjects())

    def save_subjects(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "txt files (*.txt)")
        if file_name:
            self.cohort.save_to_txt(file_name)

    def comparison(self):
        group_button = self.selected_groups_radio_button
        if group_button:
            if not self.atlas_dict:
                self.comparison_error("Atlas not loaded")
                return
            permutations = self.spinBoxPermutations.value()
            group1 = group_button.group1
            group2 = group_button.group2
            labels = ["Difference", "p-value (single-tailed)", "p-value (double-tailed)"]
            self.tableWidget_group_comparison.setRowCount(3)
            self.tableWidget_group_comparison.setVerticalHeaderLabels(labels)
            try:
                averages, stds, p_values = group1.comparison(group2, permutations=permutations)
                for i in range(len(averages[0])):
                    diff = averages[0][i] - averages[1][i]
                    item = QTableWidgetItem(str(diff))
                    self.tableWidget_group_comparison.setItem(0, i, item)
                    item = QTableWidgetItem(str(p_values[0][i]))
                    self.tableWidget_group_comparison.setItem(1, i, item)
                    item = QTableWidgetItem(str(p_values[1][i]))
                    self.tableWidget_group_comparison.setItem(2, i, item)

            except AssertionError as e:
                self.comparison_error(str(e))

    def comparison_error(self, msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle("Comparison error")
        msg_box.exec_()

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
