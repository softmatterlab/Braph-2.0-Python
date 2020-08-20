from PyQt5.QtGui import QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pyqtgraph import ColorMap
from contextlib import contextmanager

def QColor_to_list(color):
    return [color.red()/255, color.green()/255, color.blue()/255, color.alpha()/255]

def QColor_from_list(color):
    color = [int(round(v*255)) for v in color]
    return QColor(color[0], color[1], color[2], color[3])

def get_colormaps():
    colormaps = {}
    colormaps['spring'] = ColorMap([0.0, 1.0], [[255, 71, 217, 255], [255, 240, 71, 255]])
    colormaps['cool'] = ColorMap([0.0, 1.0], [[71, 245, 245, 255], [255, 71, 217, 255]])
    colormaps['hot'] = ColorMap([0.0, 0.33, 0.67, 1.0], [[0, 0, 0, 255], [255, 0, 0, 255], [255, 255, 0, 255], [255, 255, 255, 255]])
    colormaps['parula'] = ColorMap([0.0, 0.5, 1.0], [[80, 57, 240, 255], [85, 170, 128, 255], [255, 240, 71, 255]])
    return colormaps

def error_msg(title, msg, icon = QMessageBox.Critical):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

@contextmanager
def wait_cursor():
    try:
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        yield
    finally:
        QtGui.QApplication.restoreOverrideCursor()

class FloatDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[-+]?[0-9]+[.]{,1}[0-9]*'), editor)
        editor.setValidator(validator)
        return editor

class IntDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[-+]?[0-9]*'), editor)
        editor.setValidator(validator)
        return editor
