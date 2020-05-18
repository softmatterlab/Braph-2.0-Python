import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.atlas.brain_region import BrainRegion
from braphy.gui.brain_atlas_gui import BrainAtlasGui
from braphy.utility.helper_functions import abs_path_from_relative, load_nv
from braphy.gui.cohort_editor_gui import CohortEditor
from braphy.gui.graph_analysis_gui import GraphAnalysis
from braphy.gui.exit_dialog import ExitDialog
from braphy.cohort.subjects import *
from PyQt5.QtCore import Qt

brain_mesh_file_name = "meshes/BrainMesh_ICBM152.nv"
brain_mesh_file = abs_path_from_relative(__file__, brain_mesh_file_name)

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/braph.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(ExitDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.color = self.palette().color(QtGui.QPalette.Window).getRgb()

        self.init_buttons()
        self.init_animation()
        self.init_slide_show(self.palette().color(QtGui.QPalette.Window))
        self.init_slide_show_3D()
        self.stackedWidget.setCurrentIndex(0)
        self.animate = True

    def init_animation(self):
        mesh_data = load_nv(brain_mesh_file)
        self.brainWidget.set_brain_mesh(mesh_data)
        self.brainWidget.set_locked(True)
        self.brainWidget.animate(True)
        self.brainWidget.setBrainBackgroundColor(self.color)
        coords = [[22.6, -59.5, 48.1],
                  [-22.8, -60.9, 46.3],
                  [-25.8, -7.6, -31.6],
                  [26.2, -6.8, -31.9],
                  [-12.6, 22.9, 42.4],
                  [13.4, 24.7, 42.0]]
        brain_regions = []
        for c in coords:
            brain_regions.append(BrainRegion(x=c[0], y=c[1], z=c[2]))
        self.brainWidget.init_brain_regions(brain_regions, 4, [], True, False)
        self.brainWidget.change_transparency(0.6)
        self.brainWidget.setCameraPosition(distance = 275)

    def init_slide_show(self, color):
        self.slideShowWidget.set_background_color(color)

    def init_slide_show_3D(self):
        self.slideShow3DWidget.init(brain_mesh_file, self.color)

    def init_buttons(self):
        self.btnBrainAtlas.clicked.connect(self.brain_atlas)
        self.btnCohort.clicked.connect(self.cohort)
        self.btnGraphAnalysis.clicked.connect(self.graph_analysis)

        self.btnMRI.clicked.connect(self.set_MRI_btn_options)
        self.btnFMRI.clicked.connect(self.set_fMRI_btn_options)
        self.btnPET.clicked.connect(self.set_PET_btn_options)
        self.btnEEG.clicked.connect(self.set_EEG_btn_options)

        self.btnAnimation.clicked.connect(self.show_animation)
        self.btnSlideShow.clicked.connect(self.show_slide_show)
        self.btn3D.clicked.connect(self.show_slide_show_3D)

        self.btnMRI.setChecked(True)
        self.btnAnimation.setChecked(True)
        self.set_MRI_btn_options()

        self.btnPause.clicked.connect(self.pause_animation)

    def pause_animation(self):
        self.slideShow3DWidget.animate(not self.animate)
        self.animate = not self.animate


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

    def graph_analysis(self, subject_class = None):
        if not subject_class:
            subject_class = self.subject_class
        self.graph_analysis_gui = GraphAnalysis(self, subject_class)
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

    def show_animation(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_slide_show(self):
        self.stackedWidget.setCurrentIndex(2)

    def show_slide_show_3D(self):
        self.stackedWidget.setCurrentIndex(1)

def braphy_run_gui():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    braphy_run_gui()
