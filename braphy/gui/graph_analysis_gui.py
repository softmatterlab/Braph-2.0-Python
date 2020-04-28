import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.graph import *
from braphy.cohort.subjects import *
from braphy.gui.community_structure_gui import CommunityStructure
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/graph_analysis.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class GraphAnalysis(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None, subject_class = SubjectMRI):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.init_buttons()
        self.init_actions()
        self.correlationMatrixWidget.init()
        self.graphMeasuresWidget.init()

        if subject_class == SubjectMRI:
            self.correlationMatrixWidget.set_structural_view()

        self.btnViewCohort.setEnabled(False)

    def init_buttons(self):
        self.btnSelectCohort.clicked.connect(self.select_cohort)
        self.btnViewCohort.clicked.connect(self.view_cohort)
        self.btnEdit.clicked.connect(self.edit_community)
        self.btnDefault.clicked.connect(self.default)
        self.btnSubgraphAnalysis.clicked.connect(self.subgraph_analysis)
        self.btnStartAnalysis.clicked.connect(self.start_analysis)

    def init_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionImport_xml.triggered.connect(self.import_xml)
        self.actionExport_xml.triggered.connect(self.export_xml)
        self.actionQuit.triggered.connect(self.close)

        self.actionGenerate_figure.triggered.connect(self.generate_figure)

        self.actionAbout.triggered.connect(self.about)

        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPan.triggered.connect(self.pan)
        self.actionPan_x_y.triggered.connect(self.pan_x_y)
        self.actionInsert_colorbar.triggered.connect(self.insert_colorbar)

    def select_cohort(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","cohort files (*.cohort)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                self.cohort_dict = json.load(f)
            self.btnViewCohort.setEnabled(True)

    def view_cohort(self):
        pass

    def edit_community(self):
        self.community_structure_gui = CommunityStructure(self)
        self.community_structure_gui.show()

    def default(self):
        pass

    def subgraph_analysis(self):
        pass

    def start_analysis(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def import_xml(self):
        pass

    def export_xml(self):
        pass

    def generate_figure(self):
        pass

    def about(self):
        QMessageBox.about(self, 'About', 'Graph analysis editor')

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def pan(self):
        pass

    def pan_x_y(self):
        pass

    def insert_colorbar(self):
        pass

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = GraphAnalysis()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
