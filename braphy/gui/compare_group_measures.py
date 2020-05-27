import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/calculation_window.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CompareGroupMeasures(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, analysis, graph_type):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.btnCalculate.setText('Compare groups')

        self.labelMatrix.hide()
        self.labelSwaps.hide()
        self.lineEditMatrix.hide()
        self.lineEditSwaps.hide()

        self.analysis = analysis
        self.graphMeasuresWidget.init(graph_type)

        self.init_buttons()
        self.init_combo_box()

    def init_buttons(self):
        self.btnCalculate.clicked.connect(self.compare)
        self.btnResume.clicked.connect(self.resume)

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

    def compare(self):
        permutations = int(self.lineEditPermutation.text())
        sub_measures = self.graphMeasuresWidget.get_selected_measures()
        group_index_1 = self.comboBoxGroup1.currentIndex()
        group_index_2 = self.comboBoxGroup2.currentIndex()
        groups = (group_index_1, group_index_2)
        for sub_measure in sub_measures:
            measure_class = self.graphMeasuresWidget.inverted_measures_dict[sub_measure]
            self.analysis.calculate_comparison(measure_class, sub_measure, groups, permutations)
        self.textBrowser.setPlainText('DONE')

    def resume(self):
        pass

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CompareGroupMeasures()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
