import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget

qtCreatorFile = "ui_files/brain_atlas.ui" # Enter file here.
brain_mesh_file = "brain_mesh.npy"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BrainAtlas(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.init_buttons()
        self.init_brain_view()

    def init_brain_view(self):
        data = np.load(brain_mesh_file, allow_pickle=True).item()
        colors = np.array([[1,0,0,1] for i in range(len(data['faces']))])
        p = gl.GLMeshItem(vertexes=data['vertices'], faces=data['faces'], faceColors=colors, drawEdges=True, edgeColor=(0, 0, 0, 1))
        self.graphicsView.addItem(p)

    def init_buttons(self):
       print("init buttons")

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = BrainAtlas()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
