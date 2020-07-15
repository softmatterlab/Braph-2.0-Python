import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/calculation_window.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CompareWithRandomGraph(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, analysis, graph_type, update_callbacks = []):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.comboBoxGroup2.hide()
        self.labelPermutation.hide()
        self.lineEditPermutation.hide()
        self.checkBoxLongitudinal.hide()

        self.analysis = analysis
        self.graphMeasuresWidget.init(graph_type)

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CompareWithRandomGraph()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
