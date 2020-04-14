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
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.tabWidget.hide()
        self.resize(self.sizeHint())
        self.groupBox.clicked.connect(self.update_visible)
        self.update_visible(False)
        self.tabWidget.currentChanged.connect(self.tab_changed)

    def init(self, brain_widget):
        self.brain_widget = brain_widget
        self.settingsWidget.init(brain_widget)
        self.groupVisualizationWidget.init(True, self.settingsWidget)
        self.subjectVisualizationWidget.init(False, self.settingsWidget)

    def set_groups(self, groups):
        self.groupVisualizationWidget.init_list(groups)

    def set_subjects(self, subjects):
        self.subjectVisualizationWidget.init_list(subjects)

    def tab_changed(self, index):
        if index == 0:
            self.brain_widget.reset_brain_region_colors()
            self.settingsWidget.change_brain_region_size()
            self.brain_widget.enable_brain_region_selection(True)
        elif index == 1:
            self.groupVisualizationWidget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)
        elif index == 2:
            self.subjectVisualizationWidget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)
        else:
            pass

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


