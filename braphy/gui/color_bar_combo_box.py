from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, QColor_to_list, QColor_from_list
from pyqtgraph import ColorMap

class ColorBar(QtWidgets.QLabel):
    def __init__(self, parent = None, colormap = None):
        super().__init__(parent)
        self.setFixedSize(200, 20)
        if not colormap:
            colormap = ColorMap([0., 1.], [[0., 0., 0., 1.], [1., 1., 1., 1.]])
        self.set_colormap(colormap)

    def set_colormap(self, colormap):
        self.colormap = colormap
        self.update_pixmap()

    def update_pixmap(self):
        m = QtGui.QPixmap(self.width(), self.height())
        p = QtGui.QPainter(m)
        h = self.height()
        for i in range(self.width()):
            color = self.colormap.map(i/self.width(), mode='float')
            color = QColor_from_list(color)
            p.setPen(color)
            p.drawLine(i, 0, i, h)
        p.end()
        self.setPixmap(m)

    def get_QColor(self, value):
        color_list = self.colormap.map(value, mode='float')
        return QColor_from_list(color_list)

class ColorBarComboBox(QtWidgets.QComboBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setIconSize(QtCore.QSize(200, 20))
        self.colormaps = []
        self.previous_index = 0
        self.custom_color_map_callbacks = []
        self.insertSeparator(0)
        self.addItem("Custom...")
        self.currentIndexChanged.connect(self.check_create_custom_map)

    def reset(self):
        self.colormaps = []
        self.blockSignals(True)
        while self.count() > 2:
            self.removeItem(0)
        self.blockSignals(False)

    def set_custom_color_map_callbacks(self, callbacks):
        self.custom_color_map_callbacks = callbacks

    def trigger_callbacks(self, colormap):
        for callback in self.custom_color_map_callbacks:
            callback(colormap)

    def add_colormap(self, colormap):
        colorbar = ColorBar(colormap = colormap)
        return self.add_colorbar(colorbar)

    def add_colorbar(self, colorbar):
        item = QtGui.QIcon(colorbar.pixmap())
        idx = self.count()-2
        self.insertItem(idx, item, "")
        self.colormaps.append(colorbar.colormap)
        return idx

    def colormap(self):
        return self.colormaps[self.currentIndex()]

    def check_create_custom_map(self, index):
        if index == self.count()-1:
            self.create_custom_color_map()
        else:
            self.previous_index = index

    def create_custom_color_map(self):
        self.blockSignals(True)
        c = ColorMapCreator(parent = self)
        res = c.exec_()
        if res == QtWidgets.QDialog.Accepted:
            idx = self.add_colorbar(c.colorBar)
            self.trigger_callbacks(c.colorBar.colormap)
        else:
            idx = self.previous_index
        self.setCurrentIndex(idx)
        self.blockSignals(False)


ui_file = abs_path_from_relative(__file__, "ui_files/color_map_creator.ui")
Form, Base = uic.loadUiType(ui_file)

class ColorMapCreator(Base, Form):
    def __init__(self, parent = None):
        super(ColorMapCreator, self).__init__(parent)
        self.setupUi(self)
        self.btnStart.clicked.connect(self.pick_start_color)
        self.btnEnd.clicked.connect(self.pick_end_color)
        self.colorStart = self.colorBar.get_QColor(0.)
        self.colorEnd = self.colorBar.get_QColor(1.)
        self.set_btn_color(self.btnStart, self.colorStart)
        self.set_btn_color(self.btnEnd, self.colorEnd)

    def pick_start_color(self):
        color = self.pick_color()
        if color.isValid():
            self.set_btn_color(self.btnStart, color)
            self.colorStart = color
            self.update_color_bar()

    def pick_end_color(self):
        color = self.pick_color()
        if color.isValid():
            self.set_btn_color(self.btnEnd, color)
            self.colorEnd = color
            self.update_color_bar()

    def pick_color(self):
        options = QtWidgets.QColorDialog.ColorDialogOptions()
        options |= QtWidgets.QColorDialog.DontUseNativeDialog
        return QtWidgets.QColorDialog.getColor(options = options)

    def set_btn_color(self, btn, color):
        style_sheet = 'background-color: {};'.format(color.name())
        btn.setStyleSheet(style_sheet)

    def update_color_bar(self):
        colormap = ColorMap([0., 1.], [QColor_to_list(self.colorStart), QColor_to_list(self.colorEnd)])
        self.colorBar.set_colormap(colormap)
