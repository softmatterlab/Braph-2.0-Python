from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative

image_1 = "figures/betweeness.png"
image_2 = "figures/clustering.png"
image_3 = "figures/degree.png"
image_4 = "figures/eccentricity.png"
image_5 = "figures/modularity.png"
image_6 = "figures/participation.png"
image_7 = "figures/strength.png"
image_8 = "figures/triangles.png"
image_9 = "figures/untitled.png"
image_10 = "figures/zscore.png"
images = [image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10]

class SlideShowWidget(QWidget):
    def __init__(self, parent = None):
        super(SlideShowWidget, self).__init__(parent)

        self.image_files = []
        for image in images:
            self.image_files.append(abs_path_from_relative(__file__, image))

        self.label = QLabel(self)
        self.label.setGeometry(100, 50, 1000, 600)

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
        self.step += 1
        if self.step >= len(images):
            self.step = 0
