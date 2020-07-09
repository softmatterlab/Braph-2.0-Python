from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative, QColor_from_list

ui_file = abs_path_from_relative(__file__, "../ui_files/binary_plot_settings.ui")
Form, Base = uic.loadUiType(ui_file)

class BinaryPlotSettingsWidget(Base, Form):
    def __init__(self, parent = None, update_function = None):
        super(BinaryPlotSettingsWidget, self).__init__(parent)
        self.setupUi(self)

        self.set_update_function(update_function)

        self.blue = [0.3, 0.3, 1.0, 1.0]
        self.line_color = QColor_from_list(self.blue)
        self.marker_color = QColor_from_list(self.blue)
        self.ci_color = QColor_from_list(self.blue)

        self.init_color_buttons()
        self.init_check_boxes()
        self.init_sliders()
        self.init_combo_boxes()
        self.init_settings_window()

    def init_check_boxes(self):
        self.checkBoxMarkers.stateChanged.connect(self.show_markers)
        self.checkBoxLines.stateChanged.connect(self.show_lines)
        self.checkBoxCI.stateChanged.connect(self.show_ci)

    def init_color_buttons(self):
        style_sheet = 'background-color: {};'.format(QColor_from_list(self.blue).name())
        self.btnMarkersColor.setStyleSheet(style_sheet)
        self.btnMarkersColor.clicked.connect(self.pick_markers_color)
        self.btnLinesColor.setStyleSheet(style_sheet)
        self.btnLinesColor.clicked.connect(self.pick_lines_color)
        self.btnCIColor.setStyleSheet(style_sheet)
        self.btnCIColor.clicked.connect(self.pick_CI_color)

    def init_sliders(self):
        self.sliderMarkers.valueChanged.connect(self.update_function)
        self.sliderLines.valueChanged.connect(self.update_function)

    def init_combo_boxes(self):
        line_styles = ['-', '--', '-.', ':']
        for line_style in line_styles:
            self.comboBoxLines.addItem(line_style)
        marker_styles = ['o', '.', '^', 's', '*', 'P', 'D']
        for marker_style in marker_styles:
            self.comboBoxMarkers.addItem(marker_style)
        self.comboBoxLines.currentTextChanged.connect(self.update_function)
        self.comboBoxMarkers.currentTextChanged.connect(self.update_function)

    def init_settings_window(self):
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

    def show_markers(self, state):
        items = [self.btnMarkersColor, self.sliderMarkers, self.comboBoxMarkers]
        for item in items:
            item.setEnabled(state)
        self.update_function()

    def show_lines(self, state):
        items = [self.btnLinesColor, self.sliderLines, self.comboBoxLines]
        for item in items:
            item.setEnabled(state)
        self.update_function()

    def show_ci(self, state):
        items = [self.btnCIColor, self.sliderCI]
        for item in items:
            item.setEnabled(state)
        self.update_function()

    def pick_color(self):
        options = QtWidgets.QColorDialog.ColorDialogOptions()
        options |= QtWidgets.QColorDialog.DontUseNativeDialog
        return QtWidgets.QColorDialog.getColor(options = options)

    def pick_markers_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnMarkersColor.setStyleSheet(style_sheet)
            self.marker_color = color
            self.update_function()

    def pick_lines_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnLinesColor.setStyleSheet(style_sheet)
            self.line_color = color
            self.update_function()

    def pick_CI_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnCIColor.setStyleSheet(style_sheet)
            self.ci_color = color
            self.update_function()

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

    def set_update_function(self, function):
        self.update_function = function

    def get_plot_settings(self):
        settings = {}
        settings['show_markers'] = self.checkBoxMarkers.isChecked()
        settings['show_lines'] = self.checkBoxLines.isChecked()
        settings['line_color'] = self.get_line_color()
        settings['marker_color'] = self.get_marker_color()
        settings['line_style'] = self.get_line_style()
        settings['marker_style'] =  self.get_marker_style()
        settings['line_width'] = self.get_line_width()
        settings['marker_size'] = self.get_marker_size()
        return settings

    def get_line_color(self):
        return self.line_color.name()

    def get_marker_color(self):
        return self.marker_color.name()

    def get_line_style(self):
        return self.comboBoxLines.currentText()

    def get_marker_style(self):
        return self.comboBoxMarkers.currentText()

    def get_line_width(self):
        return self.sliderLines.value()

    def get_marker_size(self):
        return self.sliderMarkers.value()


