import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/calculation_window.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CalculateGroupMeasures(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, analysis, graph_type):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.comboBoxGroup2.hide()
        self.labelPermutation.hide()
        self.labelMatrix.hide()
        self.labelSwaps.hide()
        self.lineEditPermutation.hide()
        self.lineEditMatrix.hide()
        self.lineEditSwaps.hide()
        self.checkBox.hide()

        self.analysis = analysis
        self.graphMeasuresWidget.init(graph_type)

        self.init_buttons()
        self.init_combo_box()

    def init_buttons(self):
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnResume.clicked.connect(self.resume)

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)

    def calculate(self):
        sub_measures = self.graphMeasuresWidget.get_selected_measures()
        group_index = self.comboBoxGroup1.currentIndex()
        for sub_measure in sub_measures:
            measure_class = self.graphMeasuresWidget.inverted_measures_dict[sub_measure]
            self.analysis.get_measurement(measure_class, sub_measure, group_index)
        self.textBrowser.setPlainText('DONE')

    def resume(self):
        pass

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CalculateGroupMeasures()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
