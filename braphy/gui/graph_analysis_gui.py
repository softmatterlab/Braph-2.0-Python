import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from community_structure_gui import CommunityStructure

 
qtCreatorFile = "ui_files/graph_analysis.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class GraphAnalysis(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.init_buttons()

    def init_buttons(self):
       self.btnEdit.clicked.connect(self.edit_community)

    def edit_community(self):
        self.community_structure_gui = CommunityStructure(self)
        self.community_structure_gui.show()

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = GraphAnalysis()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()