from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets, Qt
from braphy.utility.helper_functions import abs_path_from_relative
from matplotlib.backends.backend_qt5agg import (
            NavigationToolbar2QT as NavigationToolbar)

ui_file = abs_path_from_relative(__file__, "../ui_files/binary_plot_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BinaryPlotWidget(Base, Form):
    def __init__(self, parent = None):
        super(BinaryPlotWidget, self).__init__(parent)
        self.setupUi(self)

        self.plot_dict = {}
        self.info_strings = []

        self.init_buttons()
        self.listWidget.itemSelectionChanged.connect(self.selection_changed)

        self.toolbar = NavigationToolbar(self.binaryPlot, self)
        self.toolbar.hide()

        self.actionLegend.triggered.connect(self.binaryPlot.show_legend)

    def init(self, analysis):
        self.analysis = analysis
        self.binaryPlot.set_x_label(self.analysis.graph_settings.rule_binary)

    def init_buttons(self):
        self.btnRemove.clicked.connect(self.remove_plot)
        self.btnClear.clicked.connect(self.clear_plot)

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
        self.binaryPlot.clear_plot()
        self.plot_dict = {}
        self.info_strings = []
        self.listWidget.clear()
        self.btnClear.setEnabled(False)
        self.actionLegend.setChecked(False)

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

    def get_actions(self):
        actions = [self.actionLegend]
        actions.extend(self.toolbar.actions())
        return actions