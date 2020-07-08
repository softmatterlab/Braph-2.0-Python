from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets, Qt
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.widgets.binary_plot_settings_widget import BinaryPlotSettingsWidget

ui_file = abs_path_from_relative(__file__, "../ui_files/binary_plot_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BinaryPlotWidget(Base, Form):
    def __init__(self, parent = None):
        super(BinaryPlotWidget, self).__init__(parent)
        self.setupUi(self)

        self.plot_dict = {}
        self.info_strings = []

        self.init_check_boxes()
        self.init_spin_boxes()
        self.init_buttons()
        self.listWidget.itemSelectionChanged.connect(self.selection_changed)

        self.binary_plot_settings_widget = BinaryPlotSettingsWidget(parent=self.binaryPlot)
        self.binary_plot_settings_widget.raise_()
        self.binary_plot_settings_widget.show()

    def init(self, analysis):
        self.analysis = analysis

    def init_check_boxes(self):
        self.checkBoxXLim.stateChanged.connect(self.set_x_lim)
        self.checkBoxYLim.stateChanged.connect(self.set_y_lim)

    def init_spin_boxes(self):
        pass

    def init_buttons(self):
        self.btnRemove.clicked.connect(self.remove_plot)
        self.btnClear.clicked.connect(self.clear_plot)

    def set_x_lim(self, checked):
        items = [self.labelXMin, self.spinBoxXMin, self.labelXMax, self.spinBoxXMax]
        for item in items:
            item.setEnabled(checked)

    def set_y_lim(self, checked):
        items = [self.labelYMin, self.spinBoxYMin, self.labelYMax, self.spinBoxYMax]
        for item in items:
            item.setEnabled(checked)

    def add_plot(self, info_string, values):
        if info_string in self.info_strings:
            return
        self.info_strings.append(info_string)
        self.listWidget.addItem(info_string)
        self.binaryPlot.add_plot(info_string, values)
        self.btnClear.setEnabled(True)

    def remove_plot(self):
        selected = self.get_selected_plots()
        for info_string in selected:
            self.binaryPlot.remove_plot(info_string)
            item = self.listWidget.findItems(info_string, Qt.Qt.MatchExactly)[0]
            self.listWidget.takeItem(self.listWidget.row(item))
            self.info_strings.remove(info_string)

    def clear_plot(self):
        #clear plot
        self.plot_dict = {}
        self.info_strings = []
        self.listWidget.clear()
        self.btnClear.setEnabled(False)

    def get_selected_plots(self):
        items = self.listWidget.selectedItems()
        items_text = [item.text() for item in items]
        return items_text

    def selection_changed(self):
        items_text = self.get_selected_plots()
        if len(items_text) > 0:
            self.btnRemove.setEnabled(True)
        else:
            self.btnRemove.setEnabled(False)

    def resizeEvent(self, event):
        self.binary_plot_settings_widget.update_move()
