#!/usr/bin/env python3

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import QFileInfo
from braphy.atlas.brain_region import BrainRegion
from braphy.gui.brain_atlas_gui import BrainAtlasGui
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
from braphy.gui.cohort_editor_gui import CohortEditor
from braphy.gui.graph_analysis_gui import GraphAnalysis
from braphy.gui.exit_dialog import ExitDialog

from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI
from PyQt5.QtCore import Qt

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/braph.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(ExitDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.subject_class = SubjectMRI

        self.color = self.palette().color(QtGui.QPalette.Window).getRgb()
        self.init_buttons()
        self.slideShowWidget.init(self.color)
        QtWidgets.qApp.focusChanged.connect(self.in_focus)

        root = QFileInfo(__file__).absolutePath()
        self.setWindowIcon(QtGui.QIcon(root+'/icons/application_icon.png'))
        self.show()

    def in_focus(self):
        if self.isActiveWindow():
            self.slideShowWidget.start_animation()
        else:
            self.slideShowWidget.pause_animation()

    def init_buttons(self):
        self.btnBrainAtlas.clicked.connect(self.brain_atlas)
        self.btnCohort.clicked.connect(self.cohort)
        self.btnGraphAnalysis.clicked.connect(self.graph_analysis)

        self.btnMRI.clicked.connect(self.set_MRI_btn_options)
        self.btnFMRI.clicked.connect(self.set_fMRI_btn_options)
        self.btnPET.clicked.connect(self.set_PET_btn_options)
        self.btnEEG.clicked.connect(self.set_EEG_btn_options)

        self.btnMRI.setChecked(True)
        self.set_MRI_btn_options()

    def brain_atlas(self):
        self.brain_atlas_gui = BrainAtlasGui(self)
        self.brain_atlas_gui.show()

    def cohort(self, subject_class = None, atlas = None, brain_mesh_data = None):
        if not subject_class:
            subject_class = self.subject_class
        if atlas:
            self.cohort_editor_gui = CohortEditor(self, subject_class = subject_class,
                                                  atlas = atlas, brain_mesh_data = brain_mesh_data)
        else:
            self.cohort_editor_gui = CohortEditor(self, subject_class = subject_class)
        self.cohort_editor_gui.show()

    def graph_analysis(self):
        self.graph_analysis_gui = GraphAnalysis(self, self.subject_class)
        self.graph_analysis_gui.show()

    def set_MRI_btn_options(self):
        self.set_btn_options("MRI")

    def set_fMRI_btn_options(self):
        self.set_btn_options("fMRI")

    def set_PET_btn_options(self):
        self.set_btn_options("PET")

    def set_EEG_btn_options(self):
        self.set_btn_options("EEG")

    def set_btn_options(self, data_type):
        self.btnCohort.setText(data_type + " Cohort")
        self.btnGraphAnalysis.setText(data_type + " Graph Analysis")
        if data_type == "MRI":
            self.subject_class = SubjectMRI
            self.subtitle.setText("Structural MRI Analysis Workflow")
        elif data_type == "fMRI":
            self.subject_class = SubjectfMRI
            self.subtitle.setText("Functional MRI Analysis Workflow")
        elif data_type == "PET":
            self.subject_class = SubjectPET
            self.subtitle.setText("PET Analysis Workflow")
        else:
            self.subject_class = SubjectEEG
            self.subtitle.setText("EEG Analysis Workflow")

def braphy_run_gui():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('braphy')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    braphy_run_gui()
