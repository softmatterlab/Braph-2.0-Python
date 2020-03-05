import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/community_structure.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CommunityStructure(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.init_buttons()

    def init_buttons(self):
        self.btnFixed.toggled.connect(self.btn_fixed_structure)
        self.btnDynamic.toggled.connect(self.btn_dynamic_structure)
        self.btnLouvain.toggled.connect(self.btn_louvain_algorithm)
        self.btnNewman.toggled.connect(self.btn_newman_algorithm)

        self.btnSet.clicked.connect(self.btn_set)
        self.btnReset.clicked.connect(self.btn_reset)
        self.btnReset.clicked.connect(self.btn_calculate)

    def btn_fixed_structure(self):
        self.btnLouvain.setDisabled(True)
        self.btnNewman.setDisabled(True)
        self.labelGamma.setDisabled(True)
        self.textEditGamma.setDisabled(True)

    def btn_dynamic_structure(self):
        self.btnLouvain.setDisabled(False)
        self.btnNewman.setDisabled(False)
        self.labelGamma.setDisabled(False)
        self.textEditGamma.setDisabled(False)

    def btn_louvain_algorithm(self):
        print("Louvain")

    def btn_newman_algorithm(self):
        print("Newman")

    def btn_set(self):
        print("set")

    def btn_reset(self):
        print("reset")

    def btn_calculate(self):
        print("calculate")





def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CommunityStructure()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
