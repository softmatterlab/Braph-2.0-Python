from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/brain_view_options_tab_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BrainViewOptionsTabWidget(Base, Form):
    def __init__(self, parent = None):
        super(BrainViewOptionsTabWidget, self).__init__(parent)
        self.setupUi(self)
        self.hide()

class BrainViewOptionsWidget(QWidget):
    def __init__(self, parent = None):
        super(BrainViewOptionsWidget, self).__init__(parent)
        self.parent = parent
        self.btnShow = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnShow.sizePolicy().hasHeightForWidth())
        self.btnShow.setSizePolicy(sizePolicy)
        self.btnShow.setMaximumSize(QtCore.QSize(30, 30))
        self.btnShow.setText("")

        self.icon_up = QtGui.QIcon()
        icon_location_up = abs_path_from_relative(__file__, "../icons/zoom_in.png")
        self.icon_up.addPixmap(QtGui.QPixmap(icon_location_up), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.icon_down = QtGui.QIcon()
        icon_location_down = abs_path_from_relative(__file__, "../icons/zoom_out.png")
        self.icon_down.addPixmap(QtGui.QPixmap(icon_location_down), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.btnShow.setIcon(self.icon_up)
        self.btnShow.setObjectName("btnShow")
        self.setAutoFillBackground(True)
        self.btnShow.clicked.connect(self.show_options)
        self.resize(30, 30)

        self.tabWidget = BrainViewOptionsTabWidget(parent = self)
        self.tabWidget.move(0, 30)

    def update_move(self):
        self.move(0, self.parent.height()-self.height())

    def show_options(self):
        if self.tabWidget.isVisible():
            self.tabWidget.hide()
            self.resize(30, 30)
            self.btnShow.setIcon(self.icon_up)
        else:
            self.tabWidget.show()
            self.resize(500, 500)
            self.btnShow.setIcon(self.icon_down)
        self.update_move()

