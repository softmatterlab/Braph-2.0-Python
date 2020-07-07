from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.widgets.binary_plot_settings_widget import BinaryPlotSettingsWidget

ui_file = abs_path_from_relative(__file__, "../ui_files/binary_plot_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BinaryPlotWidget(Base, Form):
    def __init__(self, parent = None):
        super(BinaryPlotWidget, self).__init__(parent)
        self.setupUi(self)

        self.init_check_boxes()
        self.init_list()
        self.init_spin_boxes()

        self.binary_plot_settings_widget = BinaryPlotSettingsWidget(parent=self.binaryPlot)
        self.binary_plot_settings_widget.raise_()
        self.binary_plot_settings_widget.show()

    def init(self, graph_type):
        pass

    def init_check_boxes(self):
        self.checkBoxXLim.stateChanged.connect(self.set_x_lim)
        self.checkBoxYLim.stateChanged.connect(self.set_y_lim)

    def init_list(self):
        pass

    def init_spin_boxes(self):
        pass

    def set_x_lim(self, checked):
        items = [self.labelXLim, self.spinBoxXMin, self.labelXMax, self.spinBoxXMax]
        for item in items:
            item.setEnabled(checked)

    def set_y_lim(self, checked):
        items = [self.labelYLim, self.spinBoxYMin, self.labelYMax, self.spinBoxYMax]
        for item in items:
            item.setEnabled(checked)

    def resizeEvent(self, event):
        self.binary_plot_settings_widget.update_move()
