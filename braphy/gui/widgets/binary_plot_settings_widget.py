from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative, QColor_from_list

ui_file = abs_path_from_relative(__file__, "../ui_files/binary_plot_settings.ui")
Form, Base = uic.loadUiType(ui_file)

class BinaryPlotSettingsWidget(Base, Form):
    def __init__(self, parent = None):
        super(BinaryPlotSettingsWidget, self).__init__(parent)
        self.setupUi(self)

        self.blue = [0.3, 0.3, 1.0, 1.0]
        self.init_color_buttons()

        self.icon_up = QtGui.QIcon()
        icon_location_up = abs_path_from_relative(__file__, "../icons/arrow_up.png")
        self.icon_up.addPixmap(QtGui.QPixmap(icon_location_up), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_down = QtGui.QIcon()
        icon_location_down = abs_path_from_relative(__file__, "../icons/arrow_down.png")
        self.icon_down.addPixmap(QtGui.QPixmap(icon_location_down), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnShow.setIcon(self.icon_up)

        self.setAutoFillBackground(True)
        self.resize(self.sizeHint())
        self.btnShow.clicked.connect(self.update_visible)
        self.visible = False
        self.update_visible()

    def init(self):
        pass

    def update_move(self):
        self.move(9, self.parent().height()-self.height() - 9)

    def update_visible(self):
        if self.visible:
            self.groupBox.show()
            self.btnShow.setIcon(self.icon_down)
            self.resize(self.sizeHint())
            self.visible = False
        else:
            self.groupBox.hide()
            self.btnShow.setIcon(self.icon_up)
            self.resize(100, 50)
            self.visible = True
        self.update_move()

    def pick_color(self):
        options = QtWidgets.QColorDialog.ColorDialogOptions()
        options |= QtWidgets.QColorDialog.DontUseNativeDialog
        return QtWidgets.QColorDialog.getColor(options = options)

    def init_color_buttons(self):
        style_sheet = 'background-color: {};'.format(QColor_from_list(self.blue).name())
        self.btnSymbolsColor.setStyleSheet(style_sheet)
        self.btnSymbolsColor.clicked.connect(self.pick_symbols_color)
        self.btnLinesColor.setStyleSheet(style_sheet)
        self.btnLinesColor.clicked.connect(self.pick_lines_color)
        self.btnCIColor.setStyleSheet(style_sheet)
        self.btnCIColor.clicked.connect(self.pick_CI_color)

    def pick_symbols_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnSymbolsColor.setStyleSheet(style_sheet)

    def pick_lines_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnLinesColor.setStyleSheet(style_sheet)

    def pick_CI_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnCIColor.setStyleSheet(style_sheet)

