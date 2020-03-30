from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative

image_1 = "../slide_show/degree.png"
image_2 = "../slide_show/strength.png"
image_3 = "../slide_show/eccentricity.png"
image_4 = "../slide_show/untitled.png"
image_5 = "../slide_show/triangles.png"
image_6 = "../slide_show/clustering.png"
image_7 = "../slide_show/participation.png"
image_8 = "../slide_show/betweeness.png"
image_9 = "../slide_show/modularity.png"
image_10 = "../slide_show/zscore.png"
images = [image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10]

string_1 = 'DEGREE of a node is the number of edges connected to the node. Connection weights are ignored in calculations.'
string_2 = 'STRENGTH of a node is the sum of the weights of the edges connected to the node. Number of connections are ignored in calculations.'
string_3 = 'ECCENTRICITY of a node is the maximal shortest path length between that node and any other node. If more than one path exist between a node and other node, the shortest path is chosen (red path in the figure).'
string_4 = '?'
string_5 = 'Number of TRIANGLES around a node is the number of neighbors of that node that are neightbors to each other.'
string_6 = 'CLUSTERING coefficient is the fraction of triangles around a node. It is equivalent to the fraction of the neighbors of the node that are neighbors of each other.'
string_7 = 'PARTICIPATION coefficient compares the number of links of a node has with nodes of other cluster to the number of links within its cluster. Nodes with a high participation coefficient (known as connector hubs) are connected to many clusters and are likely to facilitate global intermodular integration.'
string_8 = 'BETWEENNESS CENTRALITY of a node is the fraction of all shortest paths in the graph that contain a given node. Nodes with high values of betweenness centrality participate in a large number of shortest paths.'
string_9 = 'MODULARITY is a statistic that quantifies the degree to which the graph may be subdivided into clearly delineated groups.'
string_10 = 'Within-module degree Z-SCORE of a node shows how well connected a node is in a given cluster by comparing the degree of the node in that cluster to the average degree of all nodes in the same cluster. This measure requires a previously determined community structure.'
string_11 = 'GLOBAL EFFICIENCY is the average inverse shortest path length in the graph. It is inversely related to the characteristic path length. If more than one path exist between a node and other node, the shortest path is chosen (red path in the figure).'
string_12 = 'PATH LENGTH of a node is the average path length from that note to all other nodes. If more than one path exist between a node and other node, the shortest path is chosen (red path in the figure).'
strings = [string_1, string_2, string_3, string_4, string_5, string_6, string_7, string_8, string_9, string_10]

class SlideShowWidget(QWidget):
    def __init__(self, parent = None):
        super(SlideShowWidget, self).__init__(parent)

        self.image_files = []
        for image in images:
            self.image_files.append(abs_path_from_relative(__file__, image))

        self.label = QLabel(self)

        self.text_label = QLabel(self)
        self.text_label.setWordWrap(True)

        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.delay = 5000 # milliseconds

        self.label.show()
        self.timerEvent()

    def set_background_color(self, color):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def timerEvent(self, e=None):
        if self.step >= len(self.image_files):
            self.timer.stop()
            return
        self.timer.start(self.delay, self)
        file = self.image_files[self.step]
        pixmap = QtGui.QPixmap(file)
        scaled_pixmap = pixmap.scaled(600, 600, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)
        self.text_label.setText(strings[self.step])
        self.step += 1
        if self.step >= len(images):
            self.step = 0

    def resizeEvent(self, event):
        width = self.width()
        height = self.height()
        self.label.setGeometry(0.5*width - 300, 0.5*height - 300, 1000, 600)
        self.text_label.setGeometry(0.5*width - 250, 0.5*height + 200, 500, 100)
