import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.gui.widgets.brain_atlas_widget import BrainAtlasWidget
from braphy.gui.brain_atlas_gui import BrainAtlasGui
from braphy.atlas.brain_region import BrainRegion
import braphy.gui.icons_rc
from functools import partial
import xml.etree.ElementTree as ET
import numpy as np

from braphy.cohort.cohort import Cohort
from braphy.cohort.subjects import *

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/cohort_editor.ui")
brain_mesh_file_name_default = "meshes/BrainMesh_ICBM152.nv"
brain_mesh_file_default = abs_path_from_relative(__file__, brain_mesh_file_name_default)

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CohortEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None, subject_class = SubjectMRI, cohort = None, atlas = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)

        if cohort:
            self.cohort = cohort
            self.init_widgets()
            #self.init_cohort(cohort)
            self.set_locked(False)
        elif atlas:
            self.cohort = Cohort('Cohort', subject_class, atlas)
            self.init_widgets()
            #self.init_cohort(atlas)
            self.set_locked(False)
        else:
            self.set_locked(True)

        self.subject_class = subject_class
        if subject_class == SubjectfMRI:
            self.tabWidget.tabBar().setTabEnabled(2, False)
            self.tabWidget.tabBar().setTabEnabled(3, False)
            self.tabWidget.tabBar().setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; \
                                                   margin: 0; padding: 0; border: none;} ")

        self.brain_mesh_data = load_nv(brain_mesh_file_default)
        self.init_buttons()
        self.init_actions()
        self.init_brain_widget()

        self.file_name = None
        self.set_brain_view_actions_visible(False)
        self.tab_groups_and_demographics()
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.groupTableWidget.set_callback(self.group_table_widget_updated)
        self.groupsAndDemographicsWidget.set_callback(self.groups_and_demographics_table_updated)
        self.subjectDataWidget.set_callback(self.subject_data_table_updated)

    def to_dict(self):
        d = self.cohort.to_dict()
        return d

    def from_file(self, file_name):
        with open(file_name, 'r') as f:
            d = json.load(f)
        self.from_dict(d)
        self.init_widgets()
        self.set_locked(False)
        self.update_tables()

    def from_dict(self, d):
        self.cohort = Cohort.from_dict(d['cohort'])
        if 'brain_mesh_data' in d.keys():
            vertices = np.asarray(d['brain_mesh_data']['vertices'])
            faces = np.asarray(d['brain_mesh_data']['faces'])
            brain_mesh_data = {'vertices': vertices, 'faces': faces}
            self.brain_mesh_data = brain_mesh_data
            self.set_brain_mesh_data()
        self.labelRegionNumber.setText("Brain region number = {}".format(self.brain_region_number()))
        self.brainWidget.init_brain_regions(self.cohort.atlas.brain_regions, 4, [], False, False)

    def to_file(self, file_name):
        self.file_name = file_name
        d = {}
        d['cohort'] = self.to_dict()
        brain_mesh_data = {}
        brain_mesh_data['vertices'] = self.brain_mesh_data['vertices'].tolist()
        brain_mesh_data['faces'] = self.brain_mesh_data['faces'].tolist()
        d['brain_mesh_data'] = brain_mesh_data
        with open(file_name, 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4)

    def set_brain_mesh_data(self):
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.change_transparency()

    def init_brain_widget(self):
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.brainWidget.change_transparency(0.5)

    def init_buttons(self):
        self.btnSelectAtlas.clicked.connect(self.load_atlas)
        self.btnViewAtlas.clicked.connect(self.view_atlas)

        self.btnViewSubjects.clicked.connect(self.view_subjects)
        self.btnViewGroup.clicked.connect(self.view_group)
        self.btnViewComparison.clicked.connect(self.view_comparison)

    def init_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionClose.triggered.connect(self.close)

        self.actionLoad_subject_group_from_file.triggered.connect(self.groupTableWidget.load_subject_group)
        self.actionAdd_group.triggered.connect(self.groupTableWidget.add_group)
        self.actionRemove_group.triggered.connect(self.groupTableWidget.remove_group)
        self.actionMove_group_up.triggered.connect(self.groupTableWidget.move_group_up)
        self.actionMove_group_down.triggered.connect(self.groupTableWidget.move_group_down)
        self.actionInvert.triggered.connect(self.groupTableWidget.invert_group)
        self.actionMerge.triggered.connect(self.groupTableWidget.merge_groups)
        self.actionIntersect.triggered.connect(self.groupTableWidget.intersect_groups)

        self.actionInvert.setEnabled(False)
        self.actionMerge.setEnabled(False)
        self.actionIntersect.setEnabled(False)

        self.actionSelect_all_subjects.triggered.connect(self.groupsAndDemographicsWidget.select_all_subjects)
        self.actionClear_selection.triggered.connect(self.groupsAndDemographicsWidget.clear_subject_selection)
        self.actionAdd_subject.triggered.connect(self.groupsAndDemographicsWidget.add_subject)
        self.actionAdd_subject_above.triggered.connect(self.groupsAndDemographicsWidget.add_subjects_above)
        self.actionAdd_subject_below.triggered.connect(self.groupsAndDemographicsWidget.add_subjects_below)
        self.actionRemove_subject.triggered.connect(self.groupsAndDemographicsWidget.remove_subjects)
        self.actionMove_subject_up.triggered.connect(self.groupsAndDemographicsWidget.move_subjects_up)
        self.actionMove_subject_down.triggered.connect(self.groupsAndDemographicsWidget.move_subjects_down)
        self.actionMove_subject_to_top.triggered.connect(self.groupsAndDemographicsWidget.move_subjects_to_top)
        self.actionMove_subject_to_bottom.triggered.connect(self.groupsAndDemographicsWidget.move_subjects_to_bottom)
        self.actionNew_group_from_selection.triggered.connect(self.groupsAndDemographicsWidget.new_group_from_selected)

        self.actionGroups_and_Demographics.triggered.connect(self.tab_groups_and_demographics)
        self.actionSubject_Data.triggered.connect(self.tab_subject_data)
        self.actionGroup_Averages.triggered.connect(self.tab_group_averages)
        self.actionBrain_View.triggered.connect(self.tab_brain_view)

        self.actionGenerate_figure.triggered.connect(self.brainWidget.generate_figure)

        self.actionNew_MRI_graph_analysis.triggered.connect(self.new_MRI_graph_analysis)

        self.actionAbout.triggered.connect(self.about)

        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPanY.triggered.connect(self.pan_y)
        self.actionPanZ.triggered.connect(self.pan_z)
        self.action3D_rotation.triggered.connect(self.rotation)
        self.actionData_cursor.triggered.connect(self.data_cursor)
        self.actionInsert_colorbar.triggered.connect(self.insert_colorbar)

        group = QtWidgets.QActionGroup(self)
        for action in (self.actionZoom_in, self.actionZoom_out, self.actionPanY,
                       self.actionPanZ, self.action3D_rotation, self.actionData_cursor):
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
        self.actionPanY.setVisible(state)
        self.actionPanZ.setVisible(state)
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

    def set_locked(self, locked):
        self.locked = locked
        lock_items = [self.btnViewAtlas, self.groupTableWidget, self.groupsAndDemographicsWidget,
                      self.subjectDataWidget, self.groupAveragesWidget, self.btnViewSubjects,
                      self.btnViewGroup, self.btnViewComparison]
        for item in lock_items:
            item.setEnabled(not self.locked)
        self.disable_menu_bar(locked)

    def group_table_widget_updated(self):
        checked_groups = len(self.groupTableWidget.get_selected())
        self.actionInvert.setEnabled(checked_groups > 0)
        self.actionMerge.setEnabled(checked_groups > 1)
        self.actionIntersect.setEnabled(checked_groups > 1)

        self.groupsAndDemographicsWidget.update_table()
        self.subjectDataWidget.update_table()
        self.groupAveragesWidget.update_tables()

        self.btnSelectAtlas.setEnabled(len(self.cohort.groups) == 0 and len(self.cohort.subjects) == 0)

    def groups_and_demographics_table_updated(self):
        self.groupTableWidget.update_table()
        self.subjectDataWidget.update_table()
        self.groupAveragesWidget.update_tables()
        self.btnSelectAtlas.setEnabled(len(self.cohort.groups) == 0 and len(self.cohort.subjects) == 0)

    def subject_data_table_updated(self):
        self.groupAveragesWidget.update_tables()

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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()",
                                                      "","cohort files (*.cohort)", options=options)
        if file_name:
            self.from_file(file_name)

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "", "cohort files (*.cohort)")
        if file_name:
            self.file_name = file_name
            self.to_file(file_name)

    def save(self):
        if self.file_name:
            self.to_file(self.file_name)
        else:
            self.save_as()

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
        self.set_cursor('icons/zoom_in.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ZOOM_IN

    def zoom_out(self):
        self.set_cursor('icons/zoom_out.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ZOOM_OUT

    def pan_y(self):
        self.set_cursor('icons/hand_xy.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_PAN_Y

    def pan_z(self):
        self.set_cursor('icons/hand.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_PAN_Z

    def rotation(self):
        self.set_cursor('icons/rotate.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_ROTATE

    def data_cursor(self):
        self.set_cursor('icons/cursor.png')
        self.brainWidget.mouse_mode = BrainAtlasWidget.MOUSE_MODE_FIND

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
        if self.cohort:
            self.brain_atlas_gui = BrainAtlasGui(self, atlas = self.cohort.atlas)
            self.brain_atlas_gui.brain_mesh_data = self.brain_mesh_data
            self.brain_atlas_gui.set_brain_mesh_data()
            self.brain_atlas_gui.set_locked(True)
            self.brain_atlas_gui.show()

    def brain_region_number(self):
        n = 0
        if self.cohort.atlas:
            n = len(self.cohort.atlas.brain_regions)
        return n

    def load_atlas(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","atlas files (*.atlas)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                atlas_dict = json.load(f)

            if 'brain_mesh_data' in atlas_dict.keys():
                vertices = np.asarray(atlas_dict['brain_mesh_data']['vertices'])
                faces = np.asarray(atlas_dict['brain_mesh_data']['faces'])
                brain_mesh_data = {'vertices': vertices, 'faces': faces}
                self.brain_mesh_data = brain_mesh_data
                self.init_brain_widget()

            atlas = BrainAtlas.from_dict(atlas_dict['atlas'])
            self.cohort = Cohort('Cohort', self.subject_class, atlas)
            self.init_widgets()
            self.set_locked(False)

            self.update_tables()
            self.btnViewAtlas.setEnabled(True)
            self.labelAtlasName.setText(file_name.split('/')[-1])
            self.labelRegionNumber.setText("Brain region number = {}".format(self.brain_region_number()))
            self.brainWidget.init_brain_regions(self.cohort.atlas.brain_regions, 4, [], False, False)

    def init_widgets(self):
        self.groupTableWidget.init(self.cohort)
        self.groupsAndDemographicsWidget.init(self.cohort)
        self.subjectDataWidget.init(self.cohort)
        self.groupAveragesWidget.init(self.cohort)

    def update_tables(self, selected_groups = None, selected_subjects = None):
        if np.any(selected_groups == None):
            selected_groups = self.groupTableWidget.get_selected()
        if np.any(selected_subjects == None):
            selected_subjects = self.groupsAndDemographicsWidget.get_selected()

        self.groupTableWidget.update_table(selected_groups)
        self.groupsAndDemographicsWidget.update_table(selected_subjects)
        self.subjectDataWidget.update_table()
        self.groupAveragesWidget.update_tables()

    def disable_menu_bar(self, b):
        self.menuGroups.setDisabled(b)
        self.menuSubjects.setDisabled(b)
        self.menuView.setDisabled(b)
        self.menuBrain_View.setDisabled(b)
        self.menuGraph_Analysis.setDisabled(b)

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
