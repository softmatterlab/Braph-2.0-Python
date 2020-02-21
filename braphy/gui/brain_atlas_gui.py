import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
 
qtCreatorFile = "ui_files/brain_atlas.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class BrainAtlas(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.init_buttons()

    def init_buttons(self):
       print("init buttons")

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = BrainAtlas()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()