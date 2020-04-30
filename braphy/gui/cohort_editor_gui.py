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

from braphy.gui.widgets.brain_view_options_widget import BrainViewOptionsWidget

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/cohort_editor.ui")
brain_mesh_file_name_default = "meshes/BrainMesh_ICBM152.nv"
brain_mesh_file_default = abs_path_from_relative(__file__, brain_mesh_file_name_default)

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CohortEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None, subject_class = SubjectMRI, cohort = None, atlas = None, brain_mesh_data = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)

        if subject_class == SubjectMRI:
            self.setWindowTitle('MRI Cohort Editor')
        elif subject_class == SubjectfMRI:
            self.setWindowTitle('fMRI Cohort Editor')

        self.brain_view_options_widget = BrainViewOptionsWidget(parent=self.tabBrain)
        self.subject_class = subject_class
        if cohort:
            self.cohort = cohort
            self.init_widgets()
            self.set_locked(False)
        elif atlas:
            self.cohort = Cohort('Cohort', subject_class, atlas)
            self.brain_mesh_data = brain_mesh_data
            self.init_atlas_dependencies()
            self.init_widgets()
            self.init_brain_widget()
            self.update_tables()
            self.set_locked(False)
        else:
            self.set_locked(True)

        if subject_class == SubjectfMRI:
            self.tabWidget.removeTab(3)
            self.tabWidget.removeTab(2)

        self.init_buttons()
        self.init_actions()

        self.file_name = None
        self.set_brain_view_actions_visible(False)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.groupTableWidget.set_callback(self.group_table_widget_updated)
        self.groupsAndDemographicsWidget.set_callback(self.groups_and_demographics_table_updated)
        self.subjectDataWidget.set_callback(self.subject_data_table_updated)

        if not AppWindow:
            self.actionNew_graph_analysis.setEnabled(False)

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
        self.file_name = file_name

    def from_dict(self, d):
        self.cohort = Cohort.from_dict(d['cohort'])
        if 'brain_mesh_data' in d.keys():
            self.init_brain_mesh(d)
        self.init_atlas_dependencies()
        self.brain_view_options_widget.set_groups(self.cohort.groups)
        self.brain_view_options_widget.set_subjects(self.cohort.subjects)
        self.btnSelectAtlas.setEnabled(len(self.cohort.groups) == 0 and len(self.cohort.subjects) == 0)

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

    def init_brain_widget(self):
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.brain_view_options_widget.init(self.brainWidget)
        self.brain_view_options_widget.settingsWidget.change_transparency()
        self.brain_view_options_widget.show()

    def init_buttons(self):
        self.btnSelectAtlas.clicked.connect(self.load_atlas)
        self.btnViewAtlas.clicked.connect(self.view_atlas)

    def init_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionQuit.triggered.connect(self.close)

        self.toolBar.addSeparator()
        for action in self.brainWidget.get_actions():
            self.toolBar.addAction(action)
        self.toolBar.addSeparator()

        for action in self.brain_view_options_widget.settingsWidget.get_actions():
            self.toolBar.addAction(action)

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

        self.actionGroups_and_Demographics.triggered.connect(lambda state, x=0: self.tabWidget.setCurrentIndex(x))
        self.actionSubject_Data.triggered.connect(lambda state, x=1: self.tabWidget.setCurrentIndex(x))
        self.actionGroup_Averages.triggered.connect(lambda state, x=2: self.tabWidget.setCurrentIndex(x))
        self.actionBrain_View.triggered.connect(lambda state, x=3: self.tabWidget.setCurrentIndex(x))

        self.actionGenerate_figure.triggered.connect(self.brainWidget.generate_figure)

        self.actionNew_graph_analysis.triggered.connect(self.new_graph_analysis)

        self.actionAbout.triggered.connect(self.about)

    def set_brain_view_actions_visible(self, state):
        for action in self.brainWidget.get_actions():
            action.setVisible(state)
        for action in self.brain_view_options_widget.settingsWidget.get_actions():
            action.setVisible(state)

    def set_locked(self, locked):
        self.locked = locked
        lock_items = [self.btnViewAtlas, self.groupTableWidget, self.tabWidget, self.textCohortName]
        for item in lock_items:
            item.setEnabled(not self.locked)
        self.disable_menu_bar(locked)

    def update_group_averages_widget(self):
        if self.cohort.subject_class == SubjectMRI:
            self.groupAveragesWidget.update_tables()

    def group_table_widget_updated(self):
        checked_groups = len(self.groupTableWidget.get_selected())
        self.actionInvert.setEnabled(checked_groups > 0)
        self.actionMerge.setEnabled(checked_groups > 1)
        self.actionIntersect.setEnabled(checked_groups > 1)

        self.groupsAndDemographicsWidget.update_table()
        self.subjectDataWidget.update_table()
        self.update_group_averages_widget()

        self.btnSelectAtlas.setEnabled(len(self.cohort.groups) == 0 and len(self.cohort.subjects) == 0)
        self.brain_view_options_widget.set_groups(self.cohort.groups)
        self.brain_view_options_widget.set_subjects(self.cohort.subjects)

    def groups_and_demographics_table_updated(self):
        self.groupTableWidget.update_table()
        self.subjectDataWidget.update_table()
        self.update_group_averages_widget()
        self.btnSelectAtlas.setEnabled(len(self.cohort.groups) == 0 and len(self.cohort.subjects) == 0)
        self.brain_view_options_widget.set_subjects(self.cohort.subjects)

    def subject_data_table_updated(self):
        self.update_group_averages_widget()

    def tab_changed(self):
        self.brain_view_options_widget.update_move()
        if self.tabWidget.currentIndex() == 3:
            self.set_brain_view_actions_visible(True)
        else:
            self.set_brain_view_actions_visible(False)

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
        file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "untitled.cohort", "cohort files (*.cohort)")
        if file_name:
            self.file_name = file_name
            self.to_file(file_name)

    def save(self):
        if self.file_name:
            self.to_file(self.file_name)
        else:
            self.save_as()

    def new_graph_analysis(self):
        self.AppWindow.graph_analysis(subject_class = self.cohort.subject_class)

    def about(self):
        QMessageBox.about(self, 'About', 'Cohort Editor')

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

    def init_brain_mesh(self, d):
        vertices = np.asarray(d['brain_mesh_data']['vertices'])
        faces = np.asarray(d['brain_mesh_data']['faces'])
        brain_mesh_data = {'vertices': vertices, 'faces': faces}
        self.brain_mesh_data = brain_mesh_data
        self.init_brain_widget()

    def init_atlas_dependencies(self):
        self.labelAtlasName.setText(self.cohort.atlas.name)
        self.labelRegionNumber.setText("Brain region number = {}".format(self.brain_region_number()))
        self.textCohortName.setText(self.cohort.name)
        self.textCohortName.textChanged.connect(self.cohort.set_name)
        show_only_selected = self.brain_view_options_widget.settingsWidget.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.brain_view_options_widget.settingsWidget.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.cohort.atlas.brain_regions, 4, [], show_brain_regions, show_only_selected)

    def load_atlas(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","atlas files (*.atlas)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                atlas_dict = json.load(f)

            if 'brain_mesh_data' in atlas_dict.keys():
                self.init_brain_mesh(atlas_dict)

            atlas = BrainAtlas.from_dict(atlas_dict['atlas'])
            self.cohort = Cohort('Cohort', self.subject_class, atlas)
            self.init_atlas_dependencies()
            self.init_widgets()
            self.set_locked(False)

            self.update_tables()
            self.btnViewAtlas.setEnabled(True)

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
        self.update_group_averages_widget()

    def disable_menu_bar(self, b):
        self.menuGroups.setDisabled(b)
        self.menuSubjects.setDisabled(b)
        self.menuView.setDisabled(b)
        self.menuBrain_View.setDisabled(b)
        self.menuGraph_Analysis.setDisabled(b)

    def resizeEvent(self, event):
        self.brain_view_options_widget.update_move()

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = CohortEditor()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
