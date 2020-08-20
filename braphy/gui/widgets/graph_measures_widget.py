from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.graph.measures.measure_parser import MeasureParser
from braphy.graph.measures.measure import Measure

ui_file = abs_path_from_relative(__file__, "../ui_files/graph_measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GraphMeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(GraphMeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        size_policy = self.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)

        self.measures_dict = MeasureParser.list_measures()
        descriptions = MeasureParser.list_measures_descriptions()
        self.measures_dimensions = MeasureParser.list_measures_dimensions_str()
        self.measure_descriptions = {}
        for sub_measures in descriptions.values():
            for sub_measure, description in sub_measures.items():
                self.measure_descriptions[sub_measure] = description

    def init(self, graph_type):
        self.init_table(graph_type)
        self.init_buttons()

    def init_table(self, graph_type):
        descriptions = MeasureParser.list_measures_descriptions()
        measures_dict = MeasureParser.list_measures()
        self.measures_dimensions = MeasureParser.list_measures_dimensions()
        self.inverted_measures_dict = {}
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        measure_descriptions = {}
        for sub_measures in descriptions.values():
            for sub_measure, description in sub_measures.items():
                measure_descriptions[sub_measure] = description

        row = 0
        for measure_class, sub_measures in measures_dict[graph_type].items():
            for sub_measure in sub_measures:
                self.inverted_measures_dict[sub_measure] = measure_class
                self.tableWidget.setRowCount(row + 1)
                item = QTableWidgetItem(sub_measure)
                item.setToolTip(measure_descriptions[sub_measure])
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 0, item)
                item = QTableWidgetItem(Measure.dimensions_str(self.measures_dimensions[sub_measure]))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 1, item)
                row += 1

    def init_buttons(self):
        self.btnSelectAll.clicked.connect(self.tableWidget.selectAll)
        self.btnClearSelection.clicked.connect(self.tableWidget.clearSelection)

        self.btnSelectGlobal.clicked.connect(lambda signal, dimension=Measure.GLOBAL: self.select_dimension(dimension))
        self.btnSelectNodal.clicked.connect(lambda signal, dimension=Measure.NODAL: self.select_dimension(dimension))
        self.btnSelectBinodal.clicked.connect(lambda signal, dimension=Measure.BINODAL: self.select_dimension(dimension))

    def select_dimension(self, dimension):
        self.tableWidget.clearSelection()
        mode = self.tableWidget.selectionMode()
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for row in range(self.tableWidget.rowCount()):
            sub_measure = self.tableWidget.item(row, 0).text()
            if self.measures_dimensions[sub_measure] == dimension:
                self.tableWidget.selectRow(row)
        self.tableWidget.setSelectionMode(mode)
        self.get_selected()

    def get_selected(self):
        return self.tableWidget.get_selected()

    def get_selected_measures(self):
        selected = self.get_selected()
        selected_measures = [self.tableWidget.item(s, 0).text() for s in selected]
        return selected_measures

    def show_buttons(self):
        for btn in [self.btnSelectAll, self.btnClearSelection,
                    self.btnSelectGlobal, self.btnSelectNodal, self.btnSelectBinodal]:
            btn.show()

    def hide_buttons(self):
        for btn in [self.btnSelectAll, self.btnClearSelection,
                    self.btnSelectGlobal, self.btnSelectNodal, self.btnSelectBinodal]:
            btn.hide()
