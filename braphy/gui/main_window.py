import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from brain_atlas_gui import BrainAtlas
from cohort_editor_gui import CohortEditor
from graph_analysis_gui import GraphAnalysis
from exit_dialog import ExitDialog

qtCreatorFile = "ui_files/braph.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(ExitDialog, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.init_buttons()

    def init_buttons(self):
        self.btnBrainAtlas.clicked.connect(self.brain_atlas)
        self.btnCohort.clicked.connect(self.cohort)
        self.btnGraphAnalysis.clicked.connect(self.graph_analysis)

        self.btnMRI.clicked.connect(self.set_MRI_btn_options)
        self.btnFMRI.clicked.connect(self.set_fMRI_btn_options)
        self.btnPET.clicked.connect(self.set_PET_btn_options)
        self.btnEEG.clicked.connect(self.set_EEG_btn_options)

        self.btnAnimation.setChecked(True)
        self.btnMRI.setChecked(True)

    def brain_atlas(self):
        self.brain_atlas_gui = BrainAtlas(self)
        self.brain_atlas_gui.show()

    def cohort(self):
        self.cohort_editor_gui = CohortEditor(self)
        self.cohort_editor_gui.show()

    def graph_analysis(self):
        self.graph_analysis_gui = GraphAnalysis(self)
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
            self.subtitle.setText("Structural MRI Analysis Workflow")
        elif data_type == "fMRI":
            self.subtitle.setText("Functional MRI Analysis Workflow")
        elif data_type == "PET":
            self.subtitle.setText("PET Analysis Workflow")
        else:
            self.subtitle.setText("EEG Analysis Workflow")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
