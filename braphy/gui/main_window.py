#!/usr/bin/env python3

import sys
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import QFileInfo
from braphy.atlas.brain_region import BrainRegion
from braphy.gui.brain_atlas_gui import BrainAtlasGui
from braphy.utility.file_utility import abs_path_from_relative, load_nv, list_data_types
from braphy.gui.cohort_editor_gui import CohortEditor
from braphy.gui.graph_analysis_gui import GraphAnalysis
from braphy.gui.exit_dialog import ExitDialog

from braphy.workflows import *
from PyQt5.QtCore import Qt

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/braph.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(ExitDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
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

        button_group = QtWidgets.QButtonGroup(self)
        for data_type in list_data_types():
            btn = QtWidgets.QRadioButton()
            btn.setText(data_type)
            btn.clicked.connect(self.data_type_changed)
            button_group.addButton(btn)
            self.layoutDataTypes.addWidget(btn)
        button_group.buttons()[0].click()

    def brain_atlas(self):
        self.brain_atlas_gui = BrainAtlasGui(self)
        self.brain_atlas_gui.show()

    def cohort(self, subject_class = None, atlas = None, brain_mesh_data = None):
        if not subject_class:
            subject_class = self.subject_class
        if atlas:
            self.cohort_editor_gui = CohortEditor(subject_class = subject_class, AppWindow = self,
                                                  atlas = atlas, brain_mesh_data = brain_mesh_data)
        else:
            self.cohort_editor_gui = CohortEditor(subject_class = subject_class, AppWindow = self)
        self.cohort_editor_gui.show()

    def graph_analysis(self, cohort = None, brain_mesh_data = None):
        if not cohort:
            subject_class = self.subject_class
        else:
            subject_class = cohort.subject_class
        self.graph_analysis_gui = GraphAnalysis(subject_class = subject_class, AppWindow = self, cohort = cohort, brain_mesh_data = brain_mesh_data)
        self.graph_analysis_gui.show()

    def data_type_changed(self):
        btn = self.sender()
        data_type = btn.text()

        self.btnCohort.setText("{} Cohort".format(data_type))
        self.btnGraphAnalysis.setText("{} Graph Analysis".format(data_type))
        self.subtitle.setText("{} Analysis Workflow".format(data_type))
        self.subject_class = eval("Subject{}".format(data_type))

def braphy_run_gui():
    background_color = "white"
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('braphy')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Background, QtGui.QColor("{}".format(background_color)))
    app.setPalette(palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    braphy_run_gui()
