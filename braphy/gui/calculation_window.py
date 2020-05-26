import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/calculation_window.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CalculationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CalculationWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
