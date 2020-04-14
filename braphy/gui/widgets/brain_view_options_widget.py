from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/brain_view_options_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BrainViewOptionsWidget(Base, Form):
    def __init__(self, parent = None):
        super(BrainViewOptionsWidget, self).__init__(parent)
        '''
        icon_location_up = abs_path_from_relative(__file__, "../icons/zoom_in.png")
        icon_location_down = abs_path_from_relative(__file__, "../icons/zoom_out.png")
        self.setStyleSheet("QGroupBox::indicator {width: 14px; height: 14px;} \
                            QGroupBox::indicator:checked {image: url({icon_location_up});} \
                            QGroupBox::indicator:Unchecked {image: url({icon_location_down});}")
        '''
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.tabWidget.hide()
        self.resize(self.sizeHint())
        self.groupBox.clicked.connect(self.update_visible)
        self.update_visible(False)

    def init(self, brain_widget):
        self.settingsWidget.init(brain_widget)
        self.groupVisualizationWidget.init(True, self.settingsWidget)
        self.subjectVisualizationWidget.init(False, self.settingsWidget)

    def set_groups(self, groups):
        self.groupVisualizationWidget.init_list(groups)

    def set_subjects(self, subjects):
        self.subjectVisualizationWidget.init_list(subjects)

    def update_move(self):
        self.move(9, self.parent().height()-self.height() - 9)

    def update_visible(self, visible):
        if visible:
            self.tabWidget.show()
            self.groupBox.resize(self.groupBox.sizeHint())
            self.resize(self.sizeHint())
        else:
            self.tabWidget.hide()
            self.resize(80, 20)
        self.update_move()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
        QWidget.paintEvent(self, e)


